package com.ocado;

/**
 * Created by jose on 11/11/16.
 */
public class ClassWithPrivateMethod {

    public String greet() {
        return "hello";
    }

    private String defaultGreet() {
        return "hello world";
    }

    private String customGreet(String s) {
        return "hello " + s;
    }
}
