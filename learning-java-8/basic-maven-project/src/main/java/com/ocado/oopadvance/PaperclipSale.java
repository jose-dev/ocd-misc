package com.ocado.oopadvance;

/**
 * Created by jose on 08/12/16.
 */
public class PaperclipSale implements Sale {
    private String colour;
    private Integer amount;
    private Double unitPrice;
    private Double finalCost;

    public PaperclipSale(String colour, Integer amount, double unitPrice) {
        this.amount = amount;
        this.colour = colour;
        this.unitPrice = unitPrice;
        this.finalCost = setFinalCost();
    }

    public String getColour() {
        return colour;
    }

    public Integer getAmount() {
        return amount;
    }

    public double getUnitPrice() {
        return unitPrice;
    }

    public double getFinalCost() {
        return finalCost;
    }

    @Override
    public double setFinalCost() {
        return(amount * unitPrice);
    }

    public String toString() {
        return String.join(", ", "COLOUR: " + colour, "UNIT PRICE: " + unitPrice, "AMOUNT: " + amount, "COST: " + finalCost);
    }
}
