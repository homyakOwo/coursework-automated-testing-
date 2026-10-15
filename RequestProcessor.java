package demo;

import java.math.BigDecimal;
import java.math.RoundingMode;

/** Учебный модуль обработки заявок для IntelliJ IDEA / JUnit. */
public final class RequestProcessor {
    private RequestProcessor() { }

    public record Application(String requestId, int quantity,
                              BigDecimal unitPrice, BigDecimal discount,
                              BigDecimal total, String status) { }

    public static Application create(String requestId, int quantity,
                                     String unitPrice, String discountPercent) {
        if (requestId == null || requestId.isBlank()) {
            throw new IllegalArgumentException("Код заявки не должен быть пустым");
        }
        String code = requestId.trim();
        if (code.length() > 30) {
            throw new IllegalArgumentException("Код заявки слишком длинный");
        }
        if (quantity < 1 || quantity > 1000) {
            throw new IllegalArgumentException("Количество: от 1 до 1000");
        }
        BigDecimal price = parseNumber(unitPrice, "Цена");
        BigDecimal discount = parseNumber(discountPercent, "Скидка");
        if (price.signum() <= 0 || price.compareTo(new BigDecimal("1000000")) > 0) {
            throw new IllegalArgumentException("Цена вне допустимого диапазона");
        }
        if (discount.signum() < 0 || discount.compareTo(new BigDecimal("50")) > 0) {
            throw new IllegalArgumentException("Скидка: от 0 до 50 процентов");
        }
        BigDecimal total = price.multiply(BigDecimal.valueOf(quantity))
                .multiply(BigDecimal.ONE.subtract(discount.movePointLeft(2)))
                .setScale(2, RoundingMode.HALF_UP);
        return new Application(code, quantity, price, discount, total, "новая");
    }

    private static BigDecimal parseNumber(String value, String label) {
        try {
            return new BigDecimal(value);
        } catch (NumberFormatException | NullPointerException ex) {
            throw new IllegalArgumentException(label + ": ожидается число", ex);
        }
    }

    public static Application changeStatus(Application app, String nextStatus) {
        if (app == null) {
            throw new IllegalArgumentException("Передана не заявка");
        }
        String expected = switch (app.status()) {
            case "новая" -> "в работе";
            case "в работе" -> "выполнена";
            default -> "";
        };
        if (!expected.equals(nextStatus)) {
            throw new IllegalArgumentException("Недопустимый переход статуса");
        }
        return new Application(app.requestId(), app.quantity(), app.unitPrice(),
                app.discount(), app.total(), nextStatus);
    }
}
