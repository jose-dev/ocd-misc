package com.ocado.de.osp.carrots;

import java.time.*;
import java.util.Random;
import java.util.UUID;

class Carrot {

    private static final double MAX_HEIGHT = 18.41 * 4;

    private static final long MATURITY_TIME = 24 * 3 + 12;

    private final Type type;

    private final String id;

    private boolean alive;

    private final Instant plantTime;

    private Double height;

    private Double weight;

    private Double length;

    private Instant lastGrow;

    boolean isAlive() {
        return alive;
    }

    boolean isMature(Clock clock) {
        return Duration.between(plantTime, clock.instant()).toHours() >= MATURITY_TIME;
    }

    public Carrot(Type type, Clock clock) {
        this.type = type;
        this.id = UUID.randomUUID().toString();
        this.alive = true;
        this.plantTime = clock.instant();
        this.lastGrow = plantTime;
        this.height = 0.0;
        this.weight = 0.0;
    }

    public void updateHeight(Clock clock, int xPos, int yPos) {
        Instant now = clock.instant();

        final Long growthTime = MATURITY_TIME;
        final Long inSoilTime = 13l;
        final Double maxHeight = MAX_HEIGHT;
        if (Duration.between(plantTime, now).toHours() >= inSoilTime) {
            this.height += variateMaxHeight(maxHeight, xPos, yPos) * Duration.between(lastGrow, now).toMillis() / Duration.ofHours(growthTime - inSoilTime).toMillis();
        }
        lastGrow = now;
    }

    private Double variateMaxHeight(Double maxHeight, int xPos, int yPos) {
        return maxHeight * Soil.modifier(xPos, yPos);
    }

    void kill() {
        this.alive = false;
    }

    public void calculateProperties(Random random) {
        this.weight = 122.0 + ((height / MAX_HEIGHT) * random.nextDouble() - 0.5) * 100;
        this.length = random.nextDouble() * MAX_HEIGHT / 4;
        if (!this.isAlive()) {
            this.weight *= 0.25;
            if (this.weight == 18) {
                this.weight = 18 * random.nextDouble();
            }
            this.length *= 0.25;
        }
    }

    public enum Type {
        PURPLE, YELLOW, CHANTENAY, DANVERS, IMPERATOR, NANTES;

    }

    public Type getType() {
        return type;
    }

    public String getId() {
        return id;
    }

    public Instant getPlantTime() {
        return plantTime;
    }

    public Double getHeight() {
        return height;
    }

    public Double getWeight() {
        return weight;
    }

    public Double getLength() {
        return length;
    }

    public Instant getLastGrow() {
        return lastGrow;
    }

}
