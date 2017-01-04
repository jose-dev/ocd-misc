package com.ocado.ds.useconfig;

import org.testng.Assert;
import org.testng.annotations.Test;
import com.ocado.ds.BaseConfig;

/**
 * Created by jose on 30/12/16.
 */
public class UseConfigTest extends BaseConfig {
    @Test
    public void testSimple() {
        Assert.assertEquals(config.get("project_source"), "my-google-project");
    }
}
