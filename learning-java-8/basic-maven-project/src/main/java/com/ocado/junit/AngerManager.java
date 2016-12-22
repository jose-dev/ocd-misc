package com.ocado.junit;


import com.google.common.base.Strings;

/**
 * Created by jose on 22/12/16.
 */
public class AngerManager {
    public static String calmString(String s) {
        return Strings.isNullOrEmpty(s) ? s : s.replaceAll("!", "");
    }
}
