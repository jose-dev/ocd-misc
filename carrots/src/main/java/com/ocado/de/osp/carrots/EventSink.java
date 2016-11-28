package com.ocado.de.osp.carrots;

import com.google.common.collect.Maps;
import com.google.gson.*;
import com.google.inject.Inject;
import com.ocado.de.osp.tools.googlecloud.bigquery.BigQueryDataLoader;
import com.ocado.de.osp.tools.googlecloud.bigquery.BigQueryTableRemover;
import com.ocado.de.osp.tools.googlecloud.storage.StorageImporter;
import java.io.File;
import java.io.IOException;
import java.lang.reflect.Type;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import org.apache.commons.io.FileUtils;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.event.Level;

public class EventSink {

    private static final Logger LOG = LoggerFactory.getLogger(EventSink.class);

    private Map<String, List<String>> events = Maps.newHashMap();

    private StorageImporter storageImporter;

    private BigQueryDataLoader dataLoader;

    private Random random;

    private BigQueryTableRemover bigQueryTableRemover;

    @Inject
    public EventSink(StorageImporter storageImporter, BigQueryDataLoader dataLoader, BigQueryTableRemover bigQueryTableRemover) {
        this.storageImporter = storageImporter;
        this.dataLoader = dataLoader;
        this.random = new Random(System.currentTimeMillis());
        this.bigQueryTableRemover = bigQueryTableRemover;
    }

    public void sink(Event event) {
        String eventJson = new GsonBuilder()
                .registerTypeAdapter(Instant.class, new DateTimeSerializer())
                .create()
                .toJson(event.getAttributes());
        events.computeIfAbsent(event.partition(), partition -> new LinkedList()).add(eventJson);
        if (random.nextDouble() < 0.01) {
            events.get(event.partition()).add(eventJson);
        }
    }

    void flush() {
        CompletableFuture.allOf(events.entrySet()
                .parallelStream()
                .map(entry -> {
                    String fileName = entry.getKey() + ".json";
                    try {
                        FileUtils.writeLines(new File(System.getProperty("java.io.tmpdir") + "/" + fileName), entry.getValue());
                    } catch (IOException ex) {
                        LOG.error("Could not export {} to tmp {} directory", fileName, System.getProperty("java.io.tmpdir"));
                    }
                    StringJoiner stringJoiner = new StringJoiner("\n");
                    entry.getValue().forEach(stringJoiner::add);
                    return storageImporter.importContent("dev-atm-eu-storage", "carrots/" + fileName, stringJoiner.toString())
                            .thenCompose(location -> {
                                BigQueryDataLoader.DataLoaderParams dataLoaderParams = new BigQueryDataLoader.DataLoaderParams();
                                try {
                                    dataLoaderParams.setDataSet("carrots")
                                            .setProject("dev-atm-eu-storage")
                                            .setSourceUri(location)
                                            .setTableName(entry.getKey())
                                            .setWriteAppend(false)
                                            .setTableSchema(getSchema(entry.getKey()));
                                    LOG.info("Deleting {}", entry.getKey());
                                    return bigQueryTableRemover.removeTable("dev-atm-eu-storage", "carrots", entry.getKey())
                                            .handle((_void, error) -> {
                                                if (error != null) {
                                                    LOG.error("Error with {} : {}", entry.getKey(), error.getMessage());
                                                }
                                                return null;
                                            })
                                            .thenCompose(_void -> {
                                                LOG.info("Importing {}", entry.getKey());
                                                return dataLoader.importData(dataLoaderParams);
                                            })
                                            .exceptionally(error -> {
                                                LOG.error("Could not process " + entry.getKey(), error);
                                                return null;
                                            });
                                } catch (IOException ex) {
                                    LOG.error("Could not import location: " + location, ex);
                                    return CompletableFuture.completedFuture(null);
                                }
                            });
                })
                .toArray(CompletableFuture[]::new))
                .thenAccept(_void -> events.clear())
                .join();
    }

    private String getSchema(String key) throws IOException {
        String schemaName = "/" + StringUtils.left(key, key.length() - 9) + ".schema";
        return schemaName;
    }

    public class DateTimeSerializer implements JsonSerializer<Instant> {

        @Override
        public JsonElement serialize(Instant t, Type type, JsonSerializationContext jsc) {
            String value = DateTimeFormatter.ofPattern("YYYY-MM-dd' 'HH:mm:ss.SSS'000 UTC'").format(LocalDateTime.ofInstant(t, ZoneId.of("UTC")));
            return new JsonPrimitive(value);
        }
    }
}
