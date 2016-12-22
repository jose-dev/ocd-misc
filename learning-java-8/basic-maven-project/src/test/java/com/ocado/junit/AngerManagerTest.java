package com.ocado.junit;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
import org.testng.annotations.Test;

/**
 * Created by jose on 22/12/16.
 */
public class AngerManagerTest {
    @Test
    public void testCalmStringWithNullInput() {
        assertThat(AngerManager.calmString(null), isEmptyOrNullString());
    }
    @Test
    public void testCalmStringWithEmptyInput() {
        assertThat(AngerManager.calmString(""), isEmptyOrNullString());
    }

    @Test
    public void testCalmStringOneExclamationMark() {
        assertThat(AngerManager.calmString("Hello!"), is(equalTo("Hello")));
    }

    @Test
    public void testCalmStringManyExclamationMarks() {
        assertThat(AngerManager.calmString("Hello!!! World!!!"), is(equalTo("Hello World")));
    }
}
