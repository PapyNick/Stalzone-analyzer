from apscheduler.schedulers.blocking import BlockingScheduler
from api import get_price_history
from db import save_price_history

# Список предметов которые отслеживаем
TRACKED_ITEMS = ['0n9q']

def collect_data():
    print('Сбор данных...')
    for item_id in TRACKED_ITEMS:
        data = get_price_history(item_id)
        if data:
            save_price_history(data, item_id)
    print('Готово!')

sheduler = BlockingScheduler()
sheduler.add_job(collect_data, 'interval', minutes=15)

if __name__ == '__main__':
    print('Планировщик запущен. Первый сбор через 15 минут.')
    collect_data()
    sheduler.start()