package com.ocado.oopadvance;

import org.testng.Assert;
import org.testng.annotations.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by jose on 08/12/16.
 */
public class SaleTest {
    @Test()
    public void testCheapestWithNoSales() {
        List<Sale> s = new ArrayList<>();
        Assert.assertEquals(Sale.cheapest(s), Double.NaN);
    }

    @Test()
    public void testCheapestWithSingleSale() {
        List<Sale> s = new ArrayList<>(Arrays.asList(new CarSale("seat", 10.0, 0.0)));
        Assert.assertEquals(Sale.cheapest(s), 10.0);
    }

    @Test()
    public void testCheapestWithMultipleSales() {
        List<Sale> s = new ArrayList<>(Arrays.asList(new CarSale("seat", 10.0, 0.0),
                new PaperclipSale("red", 1000, 1.0)));
        Assert.assertEquals(Sale.cheapest(s), 10.0);
    }

    @Test
    public void testTotalCostWithNoSales() {
        List<Sale> s = new ArrayList<>();
        Assert.assertEquals(Sale.totalCost(s), 0.0);
    }

    @Test()
    public void testTotalCostWithMultipleSales() {
        List<Sale> s = new ArrayList<>(Arrays.asList(new CarSale("seat", 10.0, 0.0),
                new PaperclipSale("red", 1000, 1.0)));
        Assert.assertEquals(Sale.totalCost(s), 1010.0);
    }
}
