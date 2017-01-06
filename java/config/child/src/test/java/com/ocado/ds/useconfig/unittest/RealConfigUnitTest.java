package com.ocado.ds.useconfig.unittest;

import com.ocado.ds.useconfig.RealConfigTest;
import org.testng.Assert;
import org.testng.annotations.Test;

/**
 * Created by jose on 06/01/17.
 */
public class RealConfigUnitTest extends RealConfigTest {
    @Test
    public void testSimple() {
        Assert.assertEquals(config.get("secret_key"), "xxx");
        Assert.assertEquals(config.get("common_stuff"), "bla");
        Assert.assertEquals(config.get("project_source"), "my-google-project");
    }
}
