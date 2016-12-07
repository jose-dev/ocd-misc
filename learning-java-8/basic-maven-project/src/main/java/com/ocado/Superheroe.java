package com.ocado;

import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

/**
 * Created by jose on 07/12/16.
 */
public class Superheroe extends Person {
    private List<String> powers = new ArrayList<String>();
    private String codename = "unknown";

    public Superheroe(String firstName, String lastName) {
        super(firstName, lastName);
    }

    public Superheroe withCodename(String codename) {
        this.codename = codename;
        return this;
    }

    public Superheroe withPowers(List<String> powers) {
        this.addPowers(powers);
        return this;
    }

    public String getCodename() {
        return codename;
    }

    public List<String> getPowers() {
        return powers;
    }

    public void addPowers(List<String> powers) {
        for (String power: powers) {
            this.addPower(power);
        }
    }

    public void addPower(String power) {
        this.powers.add(power);
    }

    public String toString() {
        String powers = this.powers.size() > 0 ? this.powers.toString() : "[None]";
        return this.getCodename() + " has these powers: " + powers;
    }

}
