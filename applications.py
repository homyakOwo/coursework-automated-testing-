"""Небольшой модуль для демонстрации автоматизированного тестирования.

Правила предметной области:
- код заявки содержит от 1 до 30 символов после удаления пробелов по краям;
- количество — целое число от 1 до 1000;
- цена единицы — положительное число не более 1 000 000;
- скидка — от 0 до 50 процентов включительно;
- итог округляется до копеек по правилу ROUND_HALF_UP;
- смена статуса: новая -> в работе -> выполнена.

Программа не обращается к сети или базе данных: тесты воспроизводимы.
"""

from dataclasses import dataclass, replace
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

MAX_QUANTITY = 1000
MAX_UNIT_PRICE = Decimal("1000000")
MAX_DISCOUNT = Decimal("50")
KOP = Decimal("0.01")


@dataclass(frozen=True)
class Application:
    request_id: str
    quantity: int
    unit_price: Decimal
    discount_percent: Decimal
    total: Decimal
    status: str = "новая"


def _number(value: object, field: str) -> Decimal:
    """Безопасно преобразовать ввод в Decimal с понятной ошибкой."""
    if isinstance(value, bool):
        raise ValueError(f"{field}: ожидается число")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field}: ожидается число") from exc
    if not result.is_finite():
        raise ValueError(f"{field}: число должно быть конечным")
    return result


def create_application(
    request_id: str,
    quantity: int,
    unit_price: object,
    discount_percent: object = 0,
) -> Application:
    """Проверить заявку, рассчитать сумму и вернуть неизменяемую запись."""
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("Код заявки не должен быть пустым")
    request_id = request_id.strip()
    if len(request_id) > 30:
        raise ValueError("Код заявки не должен превышать 30 символов")
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValueError("Количество должно быть целым числом")
    if not 1 <= quantity <= MAX_QUANTITY:
        raise ValueError("Количество должно быть от 1 до 1000")
    price = _number(unit_price, "Цена")
    if not 0 < price <= MAX_UNIT_PRICE:
        raise ValueError("Цена должна быть больше 0 и не выше 1000000")
    discount = _number(discount_percent, "Скидка")
    if not 0 <= discount <= MAX_DISCOUNT:
        raise ValueError("Скидка должна быть от 0 до 50 процентов")
    total = (Decimal(quantity) * price * (Decimal("1") - discount / Decimal("100"))).quantize(
        KOP, rounding=ROUND_HALF_UP
    )
    return Application(request_id, quantity, price, discount, total)


def change_status(application: Application, next_status: str) -> Application:
    """Разрешить последовательный переход к следующему состоянию заявки."""
    transitions = {"новая": "в работе", "в работе": "выполнена", "выполнена": None}
    if not isinstance(application, Application):
        raise TypeError("Передана не заявка")
    if next_status != transitions[application.status]:
        raise ValueError(f"Недопустимый переход статуса: {application.status} -> {next_status}")
    return replace(application, status=next_status)
