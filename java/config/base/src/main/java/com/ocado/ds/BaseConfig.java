package com.ocado.ds;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * Created by jose on 30/12/16.
 */
public class BaseConfig {
    protected Properties config = new Properties();

    public BaseConfig() {
        try (InputStream in = BaseConfig.class.getResourceAsStream("/config.properties")) {
            config.load(in);
        } catch (IOException e){
            throw new RuntimeException(e);
        }
    }
}
