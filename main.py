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

delay = 5

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python main.py <token> queries,list")
        sys.exit(1)

    bot_token = sys.argv[1]
    queries = sys.argv[2].split(',')
    bot = TeleBot(token=bot_token, parse_mode="HTML")

    db.init()
    print('~~* Bot Started *~~')

    while 1:
        for q in queries:
            for x in range(0, 1):
                result = search(q)

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
                            print(coloring.yellow(f'[+] Новый товар в базе "{name}"'))
                            db.add_item(name, avg_price, min_price, max_price, rarity, traits, lvl)
                            last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            last_update = item_data['update_datetime']
                            last_update_datetime = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
                            if last_update_datetime + timedelta(days=1) < datetime.now():
                                print(coloring.gold(
                                    f'[~] Обновление товара в базе "{name}". '
                                    f'Дата последнего обновления: {last_update}'))
                                db.update_item(name,
                                               avg_price,
                                               min_price,
                                               max_price,
                                               rarity, traits, lvl)

                            # else:
                            #     print(f'[*] Не требует обновления "{name}". Пропуск')

                        # print(f"Название: {name}\n"
                        #       f"Закалка: {rarity}\n"
                        #       f"Цена: {price}x{count} = {full_price}\n"
                        #       f"Место: {location} | {guild}\n"
                        #       f"Когда видели: {last_seen}\n"
                        #       f"---------------------------\n"
                        #       f"Цена на рынке: {min_price} - {max_price}\n"
                        #       f"Средняя стоимость: {round(avg_price)}"
                        #       f"\n---------------------------\n"
                        #       f"Профит: {round(avg_price - price) * int(count)}"
                        #       )

                        if price < avg_price and db.get_show(item_hash) is None:
                            db.add_show(item_hash)
                            print(coloring.green(item))

                            img1 = Image.new("RGB", (450, 300), (0, 0, 0))
                            draw = ImageDraw.Draw(img1)
                            # rarity_txt = {
                            #     'normal': '🤍',
                            #     'fine': '💚',
                            #     'superior': '💙',
                            #     'epic': '💜',
                            #     'legendary': '💛',
                            # }
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
                                # img2 = Image.open(requests.get(img, stream=True).raw).resize((100, 100))
                                # img1.paste(img2, (int(450 / 2 - img2.width / 2), int(300 / 2 - img2.height / 2)))
                                bot.send_photo(tg_channel, img, caption=msg)

                            except:
                                bot.send_message(tg_channel, msg)

                            time.sleep(delay)

                    except Exception as e:
                        print(e)

        time.sleep(delay)
