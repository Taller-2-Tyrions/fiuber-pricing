from app.services.pricing import get_first_decimal


def test_first_decimal():

    number = 105
    assert (get_first_decimal(number) == 0)

    number = 0.1545
    assert (get_first_decimal(number) == 1)

    number = 0.01545
    assert (get_first_decimal(number) == 2)

    number = 0.003450001
    first = get_first_decimal(number)
    assert (first == 3)
    assert (round(number, first+1) == 0.0035)
