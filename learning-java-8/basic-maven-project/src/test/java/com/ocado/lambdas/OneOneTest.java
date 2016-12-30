package com.ocado.lambdas;


import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.SynchronousQueue;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
import org.hamcrest.collection.*;
import org.testng.annotations.Test;


/**
 * Created by jose on 30/12/16.
 */
public class OneOneTest {
    @Test
    public void testSortStringByLength() {
        List<String> words = new ArrayList<>(Arrays.asList("aaa", "aa", "a"));
        List<String> expect = new ArrayList<>(Arrays.asList("a", "aa", "aaa"));
        Collections.sort(words, (String a, String b) -> a.length() - b.length());
        assertThat(words, IsIterableContainingInOrder.contains(expect.toArray()));
    }

    @Test
    public void testReverseSortStringByLength() {
        List<String> words = new ArrayList<>(Arrays.asList("a", "aa", "aaa"));
        List<String> expect = new ArrayList<>(Arrays.asList("aaa", "aa", "a"));
        Collections.sort(words, (String a, String b) -> b.length() - a.length());
        assertThat(words, IsIterableContainingInOrder.contains(expect.toArray()));
    }

    @Test
    public void testSortStringByAlphabeticOrder() {
        List<String> words = new ArrayList<>(Arrays.asList("ca", "da", "aa", "ba"));
        List<String> expect = new ArrayList<>(Arrays.asList("aa", "ba", "ca", "da"));
        Collections.sort(words, (String a, String b) -> a.charAt(0) - b.charAt(0));
        assertThat(words, IsIterableContainingInOrder.contains(expect.toArray()));
    }
}
