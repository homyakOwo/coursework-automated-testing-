package demo;

import static org.junit.jupiter.api.Assertions.*;
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;

class RequestProcessorTest {
    @Test void t01ValidApplication() {
        assertEquals(new BigDecimal("200.00"),
                RequestProcessor.create("U001", 2, "100", "0").total());
    }

    @Test void t02EmptyCode() {
        assertThrows(IllegalArgumentException.class,
                () -> RequestProcessor.create(" ", 1, "100", "0"));
    }

    @Test void t03NegativeQuantity() {
        assertThrows(IllegalArgumentException.class,
                () -> RequestProcessor.create("U003", -1, "100", "0"));
    }

    @Test void t04MinimumQuantity() {
        assertEquals(new BigDecimal("10.00"),
                RequestProcessor.create("U004", 1, "10", "0").total());
    }

    @Test void t05ChangeStatus() {
        var app = RequestProcessor.create("U005", 1, "10", "0");
        assertEquals("в работе", RequestProcessor.changeStatus(app, "в работе").status());
    }

    @Test void discountMaximum() {
        assertEquals(new BigDecimal("40.00"),
                RequestProcessor.create("U006", 1, "80", "50").total());
    }

    @Test void invalidDiscount() {
        assertThrows(IllegalArgumentException.class,
                () -> RequestProcessor.create("U007", 1, "80", "51"));
    }
}
