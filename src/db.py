from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime

Base = declarative_base()


class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)


class PriceHistoryAggregated(Base):
    __tablename__ = 'price_history_aggregated'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    avg_price = Column(Float, nullable=False)
    min_price = Column(Integer, nullable=False)
    max_price = Column(Integer, nullable=False)
    total_sales = Column(Integer, nullable=False)


# Подключение к
engine = create_engine('sqlite:///stalzone.db', echo=True)


def init_db():
    Base.metadata.create_all(engine)


def save_price_history(data: dict, item_id: str):
    with Session(engine) as session:
        new_count = 0
        for entry in data['prices']:
            time = datetime.fromisoformat(entry['time'].replace('Z', '+00:00'))

            # Проверка на наличие записи в бд
            exists = session.query(PriceHistory).filter_by(
                item_id=item_id,
                time=time
            ).first()

            if not exists:
                record = PriceHistory(
                    item_id=item_id,
                    amount=entry['amount'],
                    price=entry['price'],
                    time=datetime.fromisoformat(entry['time'].replace('Z', '+00:00'))
                )
                session.add(record)
                new_count += 1

        session.commit()
    print(f'Сохранено новых данных: {new_count} для {item_id}')

if __name__ == '__main__':
    init_db()
    print('БД успешно создана!')

    # Тест сохранения
    from api import get_price_history

    data = get_price_history('0n9q')
    print('Данные от API:', data)
    if data:
        save_price_history(data, '0n9q')

    with Session(engine) as session:
        records = session.query(PriceHistory).all()
        print(f'Записей в бд: {len(records)}')
        for r in records:
            print(r.item_id, r.price, r.time)
