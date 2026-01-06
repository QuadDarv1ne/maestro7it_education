package analyzer.utils;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class StringUtilsTest {

    @Test
    public void testIsNullOrEmpty() {
        assertTrue(StringUtils.isNullOrEmpty(null));
        assertTrue(StringUtils.isNullOrEmpty(""));
        assertFalse(StringUtils.isNullOrEmpty("hello"));
        assertFalse(StringUtils.isNullOrEmpty(" "));
    }

    @Test
    public void testIsNullOrBlank() {
        assertTrue(StringUtils.isNullOrBlank(null));
        assertTrue(StringUtils.isNullOrBlank(""));
        assertTrue(StringUtils.isNullOrBlank("   "));
        assertTrue(StringUtils.isNullOrBlank("\t\n"));
        assertFalse(StringUtils.isNullOrBlank("hello"));
        assertFalse(StringUtils.isNullOrBlank(" hello "));
    }

    @Test
    public void testToLowerCase() {
        assertNull(StringUtils.toLowerCase(null));
        assertEquals("hello", StringUtils.toLowerCase("HELLO"));
        assertEquals("hello world", StringUtils.toLowerCase("Hello World"));
        assertEquals("123", StringUtils.toLowerCase("123"));
    }

    @Test
    public void testToUpperCase() {
        assertNull(StringUtils.toUpperCase(null));
        assertEquals("HELLO", StringUtils.toUpperCase("hello"));
        assertEquals("HELLO WORLD", StringUtils.toUpperCase("Hello World"));
        assertEquals("123", StringUtils.toUpperCase("123"));
    }

    @Test
    public void testTrim() {
        assertNull(StringUtils.trim(null));
        assertEquals("hello", StringUtils.trim("  hello  "));
        assertEquals("hello world", StringUtils.trim(" hello world "));
        assertEquals("", StringUtils.trim("   "));
    }

    @Test
    public void testNormalize() {
        assertNull(StringUtils.normalize(null));
        assertEquals("hello", StringUtils.normalize("héllo"));
        assertEquals("resume", StringUtils.normalize("résumé"));
    }

    @Test
    public void testCapitalize() {
        assertNull(StringUtils.capitalize(null));
        assertEquals("", StringUtils.capitalize(""));
        assertEquals("Hello", StringUtils.capitalize("hello"));
        assertEquals("Hello world", StringUtils.capitalize("hello world"));
        assertEquals("123", StringUtils.capitalize("123"));
    }
}