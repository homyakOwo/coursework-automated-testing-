namespace TestingDemo;

public record Application(string RequestId, int Quantity, decimal UnitPrice,
    decimal DiscountPercent, decimal Total, string Status = "новая");

/// <summary>Учебный модуль обработки заявок для Visual Studio / MSTest.</summary>
public static class RequestProcessor
{
    public static Application Create(string? requestId, int quantity,
        decimal unitPrice, decimal discountPercent = 0)
    {
        if (string.IsNullOrWhiteSpace(requestId))
            throw new ArgumentException("Код заявки не должен быть пустым");
        string code = requestId.Trim();
        if (code.Length > 30)
            throw new ArgumentException("Код заявки слишком длинный");
        if (quantity < 1 || quantity > 1000)
            throw new ArgumentOutOfRangeException(nameof(quantity), "Количество от 1 до 1000");
        if (unitPrice <= 0 || unitPrice > 1_000_000m)
            throw new ArgumentOutOfRangeException(nameof(unitPrice));
        if (discountPercent < 0 || discountPercent > 50)
            throw new ArgumentOutOfRangeException(nameof(discountPercent));

        decimal total = Math.Round(quantity * unitPrice *
            (1 - discountPercent / 100), 2, MidpointRounding.AwayFromZero);
        return new Application(code, quantity, unitPrice, discountPercent, total);
    }

    public static Application ChangeStatus(Application application, string nextStatus)
    {
        string? allowed = application.Status switch
        {
            "новая" => "в работе",
            "в работе" => "выполнена",
            _ => null
        };
        if (allowed != nextStatus)
            throw new InvalidOperationException("Недопустимый переход статуса");
        return application with { Status = nextStatus };
    }
}
