package com.ocado;

import org.testng.Assert;
import org.testng.annotations.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by jose on 07/12/16.
 */
public class SuperheroeTest {
    @Test()
    public void testConstructorWithNoPowers() {
        String firstName = "Pepe";
        String lastName = "Grillo";
        Superheroe p = new Superheroe(firstName, lastName);
        Assert.assertEquals(p.getFirstName(), firstName);
        Assert.assertEquals(p.getLastName(), lastName);
        Assert.assertEquals(p.getPowers(), new ArrayList<String>());
    }

    @Test()
    public void testConstructorWithPowers() {
        String firstName = "Pepe";
        String lastName = "Grillo";
        List<String> powers = new ArrayList<String>(Arrays.asList("flight", "x-vision"));
        Superheroe p = new Superheroe(firstName, lastName, powers);
        Assert.assertEquals(p.getFirstName(), firstName);
        Assert.assertEquals(p.getLastName(), lastName);
        Assert.assertEquals(p.getPowers(), powers);
    }

    @Test()
    public void testAddPower() {
        String firstName = "Pepe";
        String lastName = "Grillo";
        Superheroe p = new Superheroe(firstName, lastName);
        Assert.assertEquals(p.getPowers(), new ArrayList<String>());
        p.addPower("flight");
        Assert.assertEquals(p.getPowers(), new ArrayList<String>(Arrays.asList("flight")));
    }
}
