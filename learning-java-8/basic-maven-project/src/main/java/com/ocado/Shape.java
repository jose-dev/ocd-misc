package com.ocado;

import java.util.List;

/**
 * Created by jose on 07/12/16.
 */
public interface Shape {
    double calculateArea();

    static double sumAreas(List<Shape> shapes) {
        double sum = 0;
        for (Shape s: shapes) {
            sum += s.calculateArea();
        }

        return sum;
    }
}
