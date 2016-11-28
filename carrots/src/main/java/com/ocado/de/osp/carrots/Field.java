package com.ocado.de.osp.carrots;

import java.util.Optional;
import java.util.Random;

class Field {

    private final int width;

    private final int height;

    private final Spot[][] spots;

    private final Random random;

    private long karrotsKilled = 0l;

    Field(int width, int height) {
        this.width = width;
        this.height = height;
        spots = new Spot[width][height];
        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                spots[i][j] = new Spot(i, j);
            }
        }
        this.random = new Random(System.nanoTime());
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    boolean hasCarrot(int xPos, int yPos) {
        return spots[xPos][yPos].hasCarrot();
    }

    void plantCarrot(Carrot carrot, int xPos, int yPos) {
        spots[xPos][yPos].plantCarrot(carrot);
    }

    Carrot getCarrot(int xPos, int yPos) {
        if (spots[xPos][yPos].hasCarrot()) {
            return spots[xPos][yPos].showCarrot();
        }
        return null;
    }

    Optional<Carrot> removeCarrot(int xPos, int yPos) {
        Optional<Carrot> carrot = spots[xPos][yPos].removeCarrot();
        carrot.ifPresent(c -> c.calculateProperties(random));
        return carrot;
    }

    void killRandomCarrot() {
        if (random.nextDouble() < 0.0001) {
            Carrot carrot = spots[random.nextInt(width)][random.nextInt(height)].showCarrot();
            if (carrot != null) {
                carrot.kill();
                karrotsKilled++;
            }
        }
    }

    public long getKarrotsKilled() {
        return karrotsKilled;
    }

}
