package com.ocado.ds.useconfig;

import com.ocado.ds.BaseConfig;

import java.io.IOException;
import java.io.InputStream;

/**
 * Created by jose on 30/12/16.
 */
public class RealConfigTest extends BaseConfig {
    public RealConfigTest() {
        super();
        try (InputStream in = BaseConfig.class.getResourceAsStream("/project.properties")) {
            config.load(in);
        } catch (IOException e){
            throw new RuntimeException(e);
        }
    }
}
