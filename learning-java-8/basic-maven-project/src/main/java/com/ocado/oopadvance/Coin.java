package com.ocado.oopadvance;

import java.util.Random;

/**
 * Created by jose on 08/12/16.
 */
public enum Coin {
    HEADS, TAILS;

    private static final Random RANDOM = new Random();

    public static Coin flip() {
        if (RANDOM.nextInt(2) == 0) {
            return HEADS;
        }
        else {
            return TAILS;
        }
    }
}
