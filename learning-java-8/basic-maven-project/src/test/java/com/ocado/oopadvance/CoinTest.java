package com.ocado.oopadvance;

import org.testng.Assert;
import org.testng.annotations.Test;

/**
 * Created by jose on 08/12/16.
 */
public class CoinTest {
    @Test
    public void testFlip() {
        Coin c = Coin.TAILS;
        Assert.assertTrue(c == Coin.HEADS || c == Coin.TAILS);
    }
}
