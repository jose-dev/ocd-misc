package com.ocado.oopadvance;

import org.testng.Assert;
import org.testng.annotations.Test;

/**
 * Created by jose on 08/12/16.
 */
public class CarSaleTest {
    @Test()
    public void testConstructor() {
        String model = "seat";
        double price = 100.0;
        double discount = 10;
        CarSale c = new CarSale(model, price, discount);
        Assert.assertEquals(c.getModel(), model);
        Assert.assertEquals(c.getListPrice(), price);
        Assert.assertEquals(c.getDiscount(), discount);
        Assert.assertEquals(c.getFinalCost(), 90.0);
    }

    @Test()
    public void testToString() {
        String model = "seat";
        double price = 100.0;
        double discount = 10;
        CarSale c = new CarSale(model, price, discount);
        Assert.assertEquals(c.toString(), "MODEL: seat, PRICE: 100.0, DISCOUNT(%): 10.0, COST: 90.0");
    }
}
