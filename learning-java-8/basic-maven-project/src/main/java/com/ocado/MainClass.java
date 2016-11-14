package com.ocado;

import java.lang.reflect.Method;

/**
 * Created by jose on 03/11/16.
 */
public class MainClass {
    public static void main(String[] args) throws Exception {
        invokeMethodsWithoutReflection();
        getMethodsWithReflection();
        invokeMethodsWithReflection();
        invokeNamedMethodWithReflection();
    }


    // without reflection
    private static void invokeMethodsWithoutReflection() {
        ClassWithPrivateMethod obj = new ClassWithPrivateMethod();
        System.out.println(obj.greet());
    }

    // with reflection
    private static void getMethodsWithReflection() {
        Method methods[] = ClassWithPrivateMethod.class.getDeclaredMethods();
        for (Method m: methods) {
            System.out.println(m.toString());
        }
    }

    // with reflection
    private static void invokeMethodsWithReflection() throws Exception {
        Object foo = Class.forName("com.ocado.ClassWithPrivateMethod").newInstance();
        Method ms[] = foo.getClass().getDeclaredMethods();
        for (Method m: ms) {
            m.setAccessible(true);
            System.out.println(m.toString());
            if (m.getParameterCount() == 0) {
                System.out.println(m.invoke(foo));
            }
        }
    }

    // with reflection
    private static void invokeNamedMethodWithReflection() throws Exception {
        // string method
        Class[] cArg = new Class[1];
        cArg[0] = String.class;

        // calling method
        Object foo = Class.forName("com.ocado.ClassWithPrivateMethod").newInstance();
        Method m = foo.getClass().getDeclaredMethod("customGreet", cArg);
        m.setAccessible(true);
        System.out.println(m.toString());
        System.out.println(m.invoke(foo, "mundo!"));
    }
}

