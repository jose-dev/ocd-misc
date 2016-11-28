package com.ocado.de.osp.carrots;

import com.google.common.collect.Maps;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Map;

public class Event {

    private String name;

    private Map<String, Object> attributes = Maps.newHashMap();

    public Event(String name, Instant timestamp) {
        this.name = name + "_1_0_0";
        Map<String, Object> header = Maps.newHashMap();
        header.put("timestamp", timestamp);
        attributes.put("header", header);
    }

    public Event put(String name, Object value) {
        this.attributes.put(name, value);
        return this;
    }

    public Map<String, Object> getAttributes() {
        return attributes;
    }

    public String getName() {
        return name;
    }

    public String partition() {
        final Instant instant = (Instant) ((Map) attributes.get("header")).get("timestamp");
        return name + "_" + DateTimeFormatter.ofPattern("YYYYMMdd").format(LocalDateTime.ofInstant(instant, ZoneId.of("UTC")));
    }

}
