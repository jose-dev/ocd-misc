package com.ocado;

import org.testng.Assert;
import org.testng.annotations.Test;

public class PersonTest {
    @Test()
    public void testConstructor() {
        String firstName = "Pepe";
        String lastName = "Grillo";
        Person p = new Person(firstName, lastName);
        Assert.assertEquals(p.getFirstName(), firstName);
        Assert.assertEquals(p.getLastName(), lastName);
    }

    @Test()
    public void testGetFullName() {
        String firstName = "Pepe";
        String lastName = "Grillo";
        Person p = new Person(firstName, lastName);
        Assert.assertEquals(p.getFullName(), "Pepe Grillo");
    }
}
