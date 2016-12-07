package com.ocado;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by jose on 07/12/16.
 */
public class Superheroe extends Person {
    private List<String> powers = new ArrayList<String>();

    public Superheroe(String firstName, String lastName) {
        super(firstName, lastName);
    }

    public Superheroe(String firstName, String lastName, List<String> powers) {
        super(firstName, lastName);
        this.setPowers(powers);
    }

    public List<String> getPowers() {
        return powers;
    }

    public void setPowers(List<String> powers) {
        this.powers = powers;
    }

    public void addPower(String power) {
        this.powers.add(power);
    }

}
