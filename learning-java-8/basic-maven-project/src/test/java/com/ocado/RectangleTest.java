package com.ocado;

import org.testng.Assert;
import org.testng.annotations.Test;

/**
 * Created by jose on 07/12/16.
 */
public class RectangleTest {
    @Test()
    public void testConstructor() {
        double x = 1.0;
        double y = 2.0;
        Rectangle c = new Rectangle(x, y);
        Assert.assertEquals(c.getX(), x);
        Assert.assertEquals(c.getY(), y);
    }

    @Test()
    public void testCalculateArea() {
        double x = 2.0;
        double y = 2.0;
        Rectangle c = new Rectangle(x, y);
        Assert.assertEquals(c.calculateArea(), 4.0);
    }
}
