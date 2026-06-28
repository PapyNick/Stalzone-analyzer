import pandas as pd
from db import Session, engine, PriceHistory


def get_current_price(item_id: str) -> int:
    """ Возвращение последней цены предмета из БД """
    with Session(engine) as session:
        record = session.query(PriceHistory) \
            .filter_by(item_id=item_id) \
            .order_by(PriceHistory.time.desc()) \
            .first()

    if record:
        return record.price
    return None


def check_price_alert(item_id: str, threshold: int) -> bool:
    """Возвращает True если текущая цена ниже порога"""
    price = get_current_price(item_id)
    if price is None:
        return False
    return price <= threshold


def detect_anomaly(item_id: str, threshold_precent: float = 50.0) -> dict:
    """
    Возвращает аномалию если последняя цена отличается
    от средней цены более чем на threshold_precent процентов
    """
    with Session(engine) as session:
        record = session.query(PriceHistory)\
            .filter_by(item_id=item_id)\
            .order_by(PriceHistory.time.desc())\
            .limit(50)\
            .all()

        if len(record) < 5:
            return None

        prices = [r.price for r in record]
        avg_price = sum(prices) / len(prices)
        last_price = prices[0]

        deviation = abs(last_price - avg_price) / avg_price * 100

        if deviation >= threshold_precent:
            return {
                'item_id': item_id,
                'last_price': last_price,
                'avg_price': round(avg_price, 2),
                'deviation': round(deviation, 2)
            }
        return None


if __name__ == '__main__':
    price = get_current_price('0n9q')
    print(f'Текущая цена: {price}')
    print(f'Ниже 5000: {check_price_alert("0n9q", 5000)}')

    anoamly = detect_anomaly('0n9q')
    print(f'Аномалия: {anoamly}')