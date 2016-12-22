package com.ocado;

import org.omg.CORBA.portable.Streamable;
import org.testng.Assert;
import org.testng.annotations.Test;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by jose on 13/12/16.
 */
public class SomeCollectionTest {
    @Test
    public void testMapCaseSensitive() {
        Map<String, String> names = new HashMap<>();
        names.put("a11", "Superman");
        names.put("a22", "Batman");
        Assert.assertEquals(names.get("a11"), "Superman");
        Assert.assertFalse(names.containsKey("a00"));
    }

}
