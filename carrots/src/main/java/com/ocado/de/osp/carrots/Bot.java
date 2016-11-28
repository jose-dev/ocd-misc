package com.ocado.de.osp.carrots;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import java.time.temporal.ChronoUnit;
import java.util.Optional;
import java.util.Random;
import java.util.UUID;

public class Bot implements Comparable<Bot> {

    static Bot installOn(Field field, Integer index, Instant start, EventSink sink) {
        return new Bot(index, 0, Clock.fixed(start, ZoneId.of("UTC")), field, sink);
    }

    private int xPos;

    private int yPos;

    private Random random;

    private Clock lastActivity;

    private Clock nextActivity;

    private Field field;

    private int direction;

    private boolean shouldNotMeasure;

    private Carrot carrotInPosition;

    private String id;

    private final EventSink sink;

    Bot(int xPos, int yPos, Clock clock, Field field, EventSink sink) {
        this.xPos = xPos;
        this.yPos = yPos;
        this.lastActivity = clock;
        this.random = new Random(System.nanoTime());
        this.field = field;
        this.direction = 1;
        this.shouldNotMeasure = false;
        this.carrotInPosition = null;
        this.id = UUID.randomUUID().toString();
        this.sink = sink;
        computeNextActivityTime();
    }

    @Override
    public int compareTo(Bot o) {
        return Long.compare(nextActivity.millis(), o.nextActivity.millis());
    }

    Clock act() {
        if (field.hasCarrot(xPos, yPos)) {
            if (shouldNotMeasure) {
                if (carrotInPosition.isAlive()) {
                    if (carrotInPosition.isMature(nextActivity)) {
                        reapCarrot();
                    } else {
                        waterCarrot(carrotInPosition);
                        move();
                    }
                } else {
                    throwAwayCarrot();
                }
            } else {
                carrotInPosition = measure();
            }
            shouldNotMeasure = !shouldNotMeasure;
        } else {
            plantCarrot();
            move();
        }

        lastActivity = nextActivity;
        computeNextActivityTime();
        return lastActivity;
    }

    private void move() {
        int oldXPos = xPos;
        int oldYPos = yPos;

        yPos += direction;
        if (yPos == field.getHeight() || yPos == 0) {
            direction *= -1;
            yPos += direction;
        }

        Event event = new Event("botMoved", nextActivity.instant());
        event.put("id", this.id);
        event.put("oldX", oldXPos);
        event.put("oldY", oldYPos);
        event.put("x", xPos);
        event.put("y", yPos);
        sink.sink(event);
    }

    private void computeNextActivityTime() {
        this.nextActivity = Clock.fixed(lastActivity.instant().plus((long) (random.nextDouble() * 60 * 60 * 1000 / field.getHeight()), ChronoUnit.MILLIS), ZoneId.of("UTC"));
    }

    private void plantCarrot() {
        final Carrot carrot = new Carrot(selectType(), nextActivity);
        field.plantCarrot(carrot, xPos, yPos);

        Event event = new Event("carrotPlanted", nextActivity.instant());
        event.put("id", carrot.getId());
        event.put("rowNumber", yPos);
        event.put("spotNumber", xPos);
        event.put("type", carrot.getType().name());
        event.put("botId", this.id);
        sink.sink(event);
    }

    private Carrot measure() {
        Carrot carrot = field.getCarrot(xPos, yPos);
        carrot.updateHeight(nextActivity, xPos, yPos);

        Event event = new Event("carrotMeasured", nextActivity.instant());
        event.put("id", carrot.getId());
        event.put("height", carrot.getHeight());
        event.put("alive", carrot.isAlive());
        event.put("botId", this.id);
        sink.sink(event);

        return carrot;
    }

    private void throwAwayCarrot() {
        Optional<Carrot> carrot = field.removeCarrot(xPos, yPos);
        carrot.ifPresent(c -> {
            Event event = new Event("carrotDecayed", nextActivity.instant());
            event.put("id", c.getId());
            event.put("weight", c.getWeight());
            event.put("length", c.getLength());
            event.put("botId", this.id);
            sink.sink(event);
        });
    }

    private void waterCarrot(Carrot carrot) {
        Event event = new Event("carrotWatered", nextActivity.instant());
        event.put("id", carrot.getId());
        event.put("waterUsed", (1.0 / 3.0) * (1 + random.nextDouble()));
        event.put("botId", this.id);
        sink.sink(event);
    }

    private void reapCarrot() {
        Optional<Carrot> carrot = field.removeCarrot(xPos, yPos);
        carrot.ifPresent(c -> {
            Event event = new Event("carrotReaped", nextActivity.instant());
            event.put("id", c.getId());
            event.put("weight", c.getWeight());
            event.put("length", c.getLength());
            event.put("botId", this.id);
            sink.sink(event);
        });
    }

    private Carrot.Type selectType() {
        return Carrot.Type.values()[random.nextInt(Carrot.Type.values().length)];
    }

    public Instant getNextActivityTime() {
        return this.nextActivity.instant();
    }
}
