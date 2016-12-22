package com.ocado.junit;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

import com.google.common.collect.Sets;
import org.testng.annotations.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

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

    @Test
    public void testCalmAttendeesEmptyRoom() {
        List<String> crowd = new ArrayList<>();
        List<String> result = AngerManager.calmAttendees(crowd);
        assertThat(result.size(), is(equalTo(0)));
    }

    @Test
    public void testCalmAttendeesMixedCrowd() {
        List<String> crowd = new ArrayList<>(Arrays.asList("Democrat", "Republican", "Democrat", "Republican"));
        List<String> result = AngerManager.calmAttendees(crowd);
        assertThat(Sets.newHashSet(result).size(), is(equalTo(1)));
    }

    @Test
    public void testCalmAttendeesUniformCrowd() {
        List<String> crowd = new ArrayList<>(Arrays.asList("Democrat", "Democrat"));
        List<String> result = AngerManager.calmAttendees(crowd);
        assertThat(Sets.newHashSet(result).size(), is(equalTo(1)));
    }


}
