package com.ocado.config;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * Created by jose on 30/12/16.
 */
public class BaseTest {
    protected Properties config = new Properties();

    public BaseTest() {
        try (InputStream in = BaseTest.class.getResourceAsStream("/config.properties")) {
            config.load(in);
        } catch (IOException e){
            throw new RuntimeException(e);
        }
    }
}
