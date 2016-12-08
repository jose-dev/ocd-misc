package com.ocado;

/**
 * Created by jose on 07/12/16.
 */
public class Rectangle implements Shape {
    private double x;
    private double y;

    public Rectangle(double x, double y) {
        setX(x);
        setY(y);
    }

    public double getY() {
        return y;
    }

    public void setY(double y) {
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public void setX(double x) {
        this.x = x;
    }

    public double calculateArea() {
        return x * y;
    }
}
