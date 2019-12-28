'''
2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра
'''
import json


def write_order_to_json(item, quantity, price, buyer, date):
    '''writes new order to orders.json'''
    file_name = 'orders.json'
    json_data = json.load(open(file_name, encoding='utf-8'))
    items = []
    items.append({"item": item, "quantity": quantity, "price": price, "buyer": buyer,
                  "date": date})
    json_data['orders'] += items
    json.dump(json_data, open(file_name, mode='w', encoding='utf-8'), sort_keys=True, indent=4,ensure_ascii=False)


if __name__ == "__main__":
    write_order_to_json('printer', '10', '6700', 'Ivanov', '10.10.10')
    write_order_to_json('printer2', '11', '7700', 'Petrov', '10.10.11')
    write_order_to_json('принтер3', '12', '8700', 'Сидоров', '10.10.12')
