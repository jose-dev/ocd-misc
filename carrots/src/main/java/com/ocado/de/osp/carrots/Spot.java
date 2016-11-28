package com.ocado.de.osp.carrots;

import java.util.Optional;

public class Spot {

    private int xPos;

    private int yPos;
    
    private Optional<Carrot> carrot;

    public Spot(int xPos, int yPos) {
        this.xPos = xPos;
        this.yPos = yPos;
        carrot = Optional.empty();
    }
    
    public boolean hasCarrot() {
        return carrot.isPresent();
    }

    Optional<Carrot> removeCarrot() {
        Optional<Carrot> result = this.carrot;
        this.carrot = Optional.empty();
        return result;
    }

    void plantCarrot(Carrot carrot) {
        this.carrot = Optional.of(carrot);
    }

    Carrot showCarrot() {
        return carrot.orElse(null);
    }

}
