package com.ocado.oopadvance;

/**
 * Created by jose on 08/12/16.
 */
public class CarSale implements Sale {
    private String model;
    private Double listPrice;
    private Double discount;
    private Double finalCost;

    public CarSale(String model, double listPrice, double discount) {
        this.model = model;
        this.listPrice = listPrice;
        this.discount = discount;
        this.finalCost = setFinalCost();
    }

    @Override
    public double setFinalCost() {
        return(this.listPrice - this.listPrice * this.discount / 100.0);
    }

    public String getModel() {
        return model;
    }

    public double getDiscount() {
        return discount;
    }

    public double getListPrice() {
        return listPrice;
    }

    public double getFinalCost() {
        return finalCost;
    }

    public String toString() {
        return String.join(", ", "MODEL: " + model, "PRICE: " + listPrice, "DISCOUNT(%): " + discount, "COST: " + finalCost);
    }
}
