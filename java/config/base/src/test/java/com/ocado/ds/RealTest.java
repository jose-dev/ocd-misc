package com.ocado.ds;

import org.testng.Assert;
import org.testng.annotations.Test;

/**
 * Created by jose on 30/12/16.
 */
public class RealTest extends BaseConfig {
    @Test
    public void testSimple() {
        Assert.assertEquals(config.get("project_source"), "my-google-project");
    }
}
