package com.ocado.oopadvance;

import java.util.List;

/**
 * Created by jose on 08/12/16.
 */
public interface Sale {
    double setFinalCost();

    double getFinalCost();

    static Sale cheapest(List<Sale> sales) {
        Sale cheapest = null;
        Double c = Double.MAX_VALUE;
        for (Sale s: sales) {
            Double cost = s.getFinalCost();
            if (c > cost) {
                cheapest = s;
                c = cost;
            }
        }
        return cheapest;
    }

    static double totalCost(List<Sale> sales) {
        Double tot = 0.0;
        for (Sale s: sales) {
            tot += s.getFinalCost();
        }
        return tot;
    }
}
