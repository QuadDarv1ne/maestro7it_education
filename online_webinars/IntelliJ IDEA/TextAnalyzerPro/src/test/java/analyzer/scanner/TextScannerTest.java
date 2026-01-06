package analyzer.scanner;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.StringReader;

public class TextScannerTest {

    @Test
    public void testScanWords() {
        String input = "Hello world test";
        TextScanner scanner = new TextScanner(new StringReader(input));

        assertTrue(scanner.hasNext());
        assertEquals("Hello", scanner.nextWord());
        assertTrue(scanner.hasNext());
        assertEquals("world", scanner.nextWord());
        assertTrue(scanner.hasNext());
        assertEquals("test", scanner.nextWord());
        assertFalse(scanner.hasNext());
    }

    @Test
    public void testScanNumbers() {
        String input = "123 456 789";
        TextScanner scanner = new TextScanner(new StringReader(input));

        assertTrue(scanner.hasNext());
        assertEquals(123, scanner.nextInt());
        assertTrue(scanner.hasNext());
        assertEquals(456, scanner.nextInt());
        assertTrue(scanner.hasNext());
        assertEquals(789, scanner.nextInt());
        assertFalse(scanner.hasNext());
    }

    @Test
    public void testMixedTokens() {
        String input = "word 123 another 456";
        TextScanner scanner = new TextScanner(new StringReader(input));

        assertTrue(scanner.hasNext());
        assertEquals("word", scanner.nextWord());
        assertTrue(scanner.hasNext());
        assertEquals(123, scanner.nextInt());
        assertTrue(scanner.hasNext());
        assertEquals("another", scanner.nextWord());
        assertTrue(scanner.hasNext());
        assertEquals(456, scanner.nextInt());
        assertFalse(scanner.hasNext());
    }

    @Test
    public void testEmptyInput() {
        String input = "";
        TextScanner scanner = new TextScanner(new StringReader(input));

        assertFalse(scanner.hasNext());
    }

    @Test
    public void testWhitespaceOnly() {
        String input = "   \t\n  ";
        TextScanner scanner = new TextScanner(new StringReader(input));

        assertFalse(scanner.hasNext());
    }
}