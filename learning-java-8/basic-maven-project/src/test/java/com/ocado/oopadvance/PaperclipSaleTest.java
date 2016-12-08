package com.ocado.oopadvance;

import org.testng.Assert;
import org.testng.annotations.Test;
import org.testng.internal.junit.InexactComparisonCriteria;

/**
 * Created by jose on 08/12/16.
 */
public class PaperclipSaleTest {
    @Test()
    public void testConstructor() {
        String colour = "red";
        double price = 10.0;
        Integer amount = 10;
        PaperclipSale c = new PaperclipSale(colour, amount, price);
        Assert.assertEquals(c.getColour(), colour);
        Assert.assertEquals(c.getUnitPrice(), price);
        Assert.assertEquals(c.getAmount(), amount);
        Assert.assertEquals(c.getFinalCost(), 100.0);
    }

    @Test()
    public void testToString() {
        String colour = "red";
        double price = 10.0;
        Integer amount = 10;
        PaperclipSale c = new PaperclipSale(colour, amount, price);
        Assert.assertEquals(c.toString(), "COLOUR: red, UNIT PRICE: 10.0, AMOUNT: 10, COST: 100.0");
    }
}
