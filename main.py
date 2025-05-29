import sys
import time
import hashlib
from datetime import datetime, timedelta

import coloring
from telebot import TeleBot

from settings import tg_channel
from ttp import db

from ttp.parser import search
from ttp.utils import robust_weighted_average


def error(m):
    print(coloring.red(f"[{datetime.now()}]\n" + m))

def info(m):
    print(coloring.gold(f"[{datetime.now()}]\n" + m))

def success(m):
    print(coloring.green(f"[{datetime.now()}]\n" + m))

delay = 5

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python main.py <token> queries,list")
        sys.exit(1)

    bot_token = sys.argv[1]
    queries = sys.argv[2].split(',')
    bot = TeleBot(token=bot_token, parse_mode="HTML")

    db.init()
    info('~~* Bot Started *~~')

    while 1:
        for q in queries:
            for x in range(0, 1):
                try:
                    result = search(q)
                except Exception as e:
                    error(f"result = search(q)\n" + str(e))
                    continue

                if not result["data"]:
                    continue
                data: list[dict] = result["data"]

                prices_list = [int(item["price"].replace(",", '')) for item in data]
                min_price = min(*prices_list)
                max_price = max(*prices_list)
                avg_price = round(robust_weighted_average(prices_list))

                for item in data:
                    try:
                        name = item["name"]
                        price = int(item["price"].replace(',', ''))
                        count = int(item["amount"])
                        full_price = price * count
                        location = f"{item['trader_zone']} | {item['trader_location']}"
                        guild = item['guild']
                        img = f"https://eso-hub.com{item['icon']}"
                        rarity = str(item['quality'])
                        traits = ''
                        lvl = str(item['level'])
                        last_seen = item['last_seen']

                        item_data = db.get_item(name, rarity, traits, lvl)
                        item_hash = f'{name}:{price}:{location}:{guild}:{rarity}:{traits}:{lvl}:{full_price}'
                        item_hash = str(hashlib.md5(item_hash.encode()).hexdigest())

                        if item_data is None:
                            info(f'[+] Новый товар в базе "{name}"')
                            db.add_item(name, avg_price, min_price, max_price, rarity, traits, lvl)
                            last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            last_update = item_data['update_datetime']
                            last_update_datetime = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
                            if last_update_datetime + timedelta(days=1) < datetime.now():
                                info(
                                    f'[~] Обновление товара в базе "{name}". '
                                    f'Дата последнего обновления: {last_update}')
                                db.update_item(name,
                                               avg_price,
                                               min_price,
                                               max_price,
                                               rarity, traits, lvl)

                        if price < avg_price and db.get_show(item_hash) is None:
                            db.add_show(item_hash)
                            log_msg = (f"{name} x{count}\n"
                                       f"Price: {price} | Avg: {avg_price}\n"
                                       f"{location} - {guild} | {last_seen}\n")
                            success(log_msg)

                            rarity_txt = {
                                "1": '🤍',
                                "2": '💚',
                                "3": '💙',
                                "4": '💜',
                                "`5`": '💛',
                            }
                            #
                            msg = f"{rarity_txt[rarity]} <b>{name}</b>\n" \
                                  f"➖➖➖➖➖➖➖➖➖\n" \
                                  f"🤑 <b>Profit:</b> ~ {round(avg_price - price) * int(count)}\n" \
                                  f"📍 <b>Location:</b> {location}\n" \
                                  f"👨‍👨‍👦‍👦 <b>Guild:</b> {guild}\n" \
                                  f"Last seen: {last_seen}\n" \
                                  f"➖➖➖➖➖➖➖➖➖\n" \
                                  f"🔹 <b>Price for one:</b> {price}\n" \
                                  f"🔹 <b>Count:</b> {count}\n" \
                                  f"🔹 <b>Full price:</b> {full_price}\n" \
                                  f"➖➖➖➖➖➖➖➖➖\n" \
                                  f"🔸 <b>Average price:</b> {avg_price}\n" \
                                  f"🔸 <b>Range:</b> {min_price} - {max_price}\n"

                            try:
                                bot.send_photo(tg_channel, img, caption=msg)

                            except:
                                bot.send_message(tg_channel, msg)

                            time.sleep(delay)

                    except Exception as e:
                        error("loop error: " + str(e))

        time.sleep(delay)
