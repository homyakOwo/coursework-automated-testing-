"""20 независимых тестов T01-T20 учебного модуля заявок."""

from decimal import Decimal

import pytest

from src.applications import Application, change_status, create_application


def test_t01_valid_application():
    app = create_application("U001", 2, "100.00")
    assert app.request_id == "U001" and app.total == Decimal("200.00")


def test_t02_empty_required_code():
    with pytest.raises(ValueError, match="не должен быть пустым"):
        create_application("", 1, "100")


def test_t03_negative_quantity():
    with pytest.raises(ValueError, match="от 1 до 1000"):
        create_application("U003", -1, "100")


def test_t04_minimum_quantity_boundary():
    assert create_application("U004", 1, "10").total == Decimal("10.00")


def test_t05_change_status():
    app = create_application("U005", 1, "10")
    assert change_status(app, "в работе").status == "в работе"


def test_t06_blank_code_with_spaces():
    with pytest.raises(ValueError, match="не должен быть пустым"):
        create_application("   ", 1, "10")


def test_t07_code_is_trimmed():
    assert create_application("  U007  ", 1, "10").request_id == "U007"


def test_t08_code_too_long():
    with pytest.raises(ValueError, match="30 символов"):
        create_application("A" * 31, 1, "10")


def test_t09_maximum_quantity_boundary():
    assert create_application("U009", 1000, "1").total == Decimal("1000.00")


def test_t10_quantity_above_maximum():
    with pytest.raises(ValueError, match="от 1 до 1000"):
        create_application("U010", 1001, "1")


def test_t11_fractional_quantity_rejected():
    with pytest.raises(ValueError, match="целым числом"):
        create_application("U011", 1.5, "10")


def test_t12_boolean_quantity_rejected():
    with pytest.raises(ValueError, match="целым числом"):
        create_application("U012", True, "10")


def test_t13_zero_price_rejected():
    with pytest.raises(ValueError, match="больше 0"):
        create_application("U013", 1, "0")


def test_t14_invalid_price_rejected():
    with pytest.raises(ValueError, match="ожидается число"):
        create_application("U014", 1, "ошибка")


def test_t15_price_above_maximum():
    with pytest.raises(ValueError, match="не выше"):
        create_application("U015", 1, "1000000.01")


def test_t16_discount_zero():
    assert create_application("U016", 2, "75", 0).total == Decimal("150.00")


def test_t17_discount_maximum_boundary():
    assert create_application("U017", 1, "80", 50).total == Decimal("40.00")


def test_t18_discount_above_maximum():
    with pytest.raises(ValueError, match="от 0 до 50"):
        create_application("U018", 1, "80", 50.01)


def test_t19_decimal_rounding():
    assert create_application("U019", 1, "0.005").total == Decimal("0.01")


def test_t20_complete_status_flow_and_no_mutation():
    initial = create_application("U020", 1, "10")
    in_progress = change_status(initial, "в работе")
    completed = change_status(in_progress, "выполнена")
    assert (initial.status, in_progress.status, completed.status) == (
        "новая", "в работе", "выполнена"
    )
    with pytest.raises(ValueError, match="Недопустимый переход"):
        change_status(completed, "в работе")
