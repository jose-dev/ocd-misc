package com.ocado.junit;


import com.google.common.base.Strings;
import com.google.common.collect.Sets;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

import java.util.List;

/**
 * Created by jose on 22/12/16.
 */
public class AngerManager {
    public static String calmString(String s) {
        return Strings.isNullOrEmpty(s) ? s : s.replaceAll("!", "");
    }

    public static List<String> calmAttendees(List<String> crowd) {
        if (Sets.newHashSet(crowd).size() < 2) {
            return crowd;
        }
        else {
            String chosenParty = ( new Random().nextBoolean() ) ? "Republican" : "Democrat";
            return remove(crowd, chosenParty);
        }
    }

    private static List<String> remove(List<String> l, String s) {
        l.removeAll(new ArrayList<String>(Arrays.asList(s)));
        return l;
    }
}
