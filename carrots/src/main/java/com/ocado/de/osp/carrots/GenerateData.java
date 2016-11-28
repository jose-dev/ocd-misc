package com.ocado.de.osp.carrots;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.LoggerContext;
import com.google.inject.Guice;
import com.google.inject.Injector;
import java.time.*;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.PriorityQueue;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class GenerateData {

    private static final Logger LOG = LoggerFactory.getLogger(GenerateData.class);

    public static void main(String[] args) {
        LoggerContext lc = (LoggerContext) LoggerFactory.getILoggerFactory();
        lc.getLogger("ROOT").setLevel(Level.INFO);

        int fieldWidth = 100;
        int fieldHeight = 100;

        final Field field = new Field(fieldWidth, fieldHeight);

        final Instant simulationStart = LocalDateTime.of(2016, 6, 7, 0, 0).toInstant(ZoneOffset.UTC);
        final Instant simulationEnd = LocalDateTime.of(2016, 6, 17, 0, 0).toInstant(ZoneOffset.UTC);

        Injector injector = Guice.createInjector(new CarrotsModule());
        EventSink sink = injector.getInstance(EventSink.class);
        final List<Bot> bots = IntStream.range(0, fieldWidth)
                .boxed()
                .map(index -> Bot.installOn(field, index, simulationStart, sink))
                .collect(Collectors.toList());

        PriorityQueue<Bot> actionQueue = new PriorityQueue(bots);
        Instant checkpoint = simulationStart;
        long ticks = 0;

        Bot nextBot = actionQueue.poll();
        while (nextBot.getNextActivityTime().isBefore(simulationEnd)) {
            if (Duration.between(checkpoint, nextBot.getNextActivityTime()).toDays() >= 1) {
                LOG.info("Flush checkpoint @ time {}", nextBot.getNextActivityTime());

                checkpoint = checkpoint.plus(1, ChronoUnit.DAYS);
                sink.flush();
            }
            nextBot.act();
            actionQueue.add(nextBot);
            field.killRandomCarrot();
            ticks++;
            nextBot = actionQueue.poll();
        }
        LOG.info("Total clock ticks {}", ticks);
        LOG.info("Dead carrots: {}", field.getKarrotsKilled());
        sink.flush();
    }

}
