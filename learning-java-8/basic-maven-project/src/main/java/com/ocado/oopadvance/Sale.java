package com.ocado.oopadvance;

import java.util.List;

/**
 * Created by jose on 08/12/16.
 */
public interface Sale {
    double setFinalCost();

    double getFinalCost();

    static double cheapest(List<Sale> sales) {
        Double c = Double.NaN;
        for (Sale s: sales) {
            Double cost = s.getFinalCost();
            if (c.isNaN() || c > cost) {
                c = cost;
            }
        }
        return c;
    }

    static double totalCost(List<Sale> sales) {
        Double tot = 0.0;
        for (Sale s: sales) {
            tot += s.getFinalCost();
        }
        return tot;
    }
}
