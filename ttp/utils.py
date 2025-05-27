from typing import List


def price_to_float(price_str: str) -> float:
    """Конвертирует строку цены в число."""
    return float(price_str.replace(",", "").replace(" ", ""))


def robust_weighted_average(prices: List[int], trim_percent: float = 0.1) -> float:
    """
    Вычисляет устойчивое среднее, учитывающее плотность распределения цен.

    Алгоритм:
    1. Удаляет верхние и нижние `trim_percent` цен (игнорирует выбросы).
    2. Взвешивает оставшиеся цены по их плотности (близости к другим значениям).

    Args:
        items: Список товаров.
        trim_percent: Доля цен для отсечения с каждого конца (0.1 = 10%).

    Returns:
        Устойчивое среднее значение.
    """
    if not prices:
        return 0.0

    prices_sorted = sorted(prices)

    # Шаг 1: Усечение выбросов
    n_trim = int(len(prices_sorted) * trim_percent)
    trimmed_prices = prices_sorted[n_trim:-n_trim] if n_trim else prices_sorted

    # Шаг 2: Расчет весов на основе плотности (близости к другим ценам)
    weights = []
    for price in trimmed_prices:
        # Вес = количество цен в окрестности ±20% от текущей цены
        lower, upper = price * 0.8, price * 1.2
        weight = sum(1 for p in trimmed_prices if lower <= p <= upper)
        weights.append(weight)

    # Нормализация весов
    total_weight = sum(weights)
    weighted_avg = sum(p * w for p, w in zip(trimmed_prices, weights)) / total_weight
    return weighted_avg
