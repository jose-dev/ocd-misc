package com.ocado;

import org.testng.Assert;
import org.testng.annotations.Test;

/**
 * Created by jose on 07/12/16.
 */
public class SquareTest {
    @Test()
    public void testConstructor() {
        double x = 1.0;
        Square c = new Square(x);
        Assert.assertEquals(c.getX(), x);
        Assert.assertEquals(c.getY(), x);
    }

    @Test()
    public void testCalculateArea() {
        double x = 2.0;
        Square c = new Square(x);
        Assert.assertEquals(c.calculateArea(), 4.0);
    }
}
