package com.ocado;


import org.testng.Assert;
import org.testng.annotations.Test;

public class CircleTest {
    @Test()
    public void testConstructor() {
        double radius = 1.0;
        Circle c = new Circle(radius);
        Assert.assertEquals(c.getRadius(), radius);
    }

    @Test()
    public void testCalculateArea() {
        double radius = 1.0;
        Circle c = new Circle(radius);
        Assert.assertEquals(Math.PI, c.calculateArea());
    }
}
