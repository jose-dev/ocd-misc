package com.ocado;

import org.testng.Assert;
import org.testng.annotations.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by jose on 07/12/16.
 */
public class ShapeTest {
    @Test()
    public void testsumAreas() {
        List<Shape> s = new ArrayList<Shape>(Arrays.asList(new Circle(1.0),
                new Rectangle(2.0, 2.0),
                new Square(3.0)));
        double sum = Shape.sumAreas(s);
        Assert.assertTrue(16.1 <= sum && sum <= 16.2);
    }
}
