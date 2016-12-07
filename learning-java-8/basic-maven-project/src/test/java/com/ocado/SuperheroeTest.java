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
        Assert.assertEquals(p.getCodename(), "unknown");
        Assert.assertEquals(p.getPowers(), new ArrayList<String>());
        Assert.assertEquals(p.toString(), "unknown has these powers: [None]");
    }

    @Test()
    public void testConstructorWithPowers() {
        String firstName = "Pepe";
        String lastName = "Grillo";
        String codename = "Supermeh";
        List<String> powers = new ArrayList<String>(Arrays.asList("flight", "x-vision"));
        Superheroe p = new Superheroe(firstName, lastName).withCodename(codename).withPowers(powers);
        Assert.assertEquals(p.getFirstName(), firstName);
        Assert.assertEquals(p.getLastName(), lastName);
        Assert.assertEquals(p.getPowers(), powers);
        Assert.assertEquals(p.getCodename(), codename);
    }

    @Test()
    public void testAddPower() {
        String firstName = "Pepe";
        String lastName = "Grillo";
        Superheroe p = new Superheroe(firstName, lastName);
        Assert.assertEquals(p.getPowers(), new ArrayList<String>());
        p.addPower("flight");
        Assert.assertEquals(p.getPowers(), new ArrayList<String>(Arrays.asList("flight")));
        Assert.assertEquals(p.toString(), "unknown has these powers: [flight]");
    }

    @Test()
    public void testAddPowers() {
        String firstName = "Pepe";
        String lastName = "Grillo";
        List<String> powers = new ArrayList<String>(Arrays.asList("flight", "x-vision"));
        Superheroe p = new Superheroe(firstName, lastName);
        Assert.assertEquals(p.getPowers(), new ArrayList<String>());
        p.addPowers(powers);
        Assert.assertEquals(p.getPowers(), powers);
        Assert.assertEquals(p.toString(), "unknown has these powers: [flight, x-vision]");
    }
}
