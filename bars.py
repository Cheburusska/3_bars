import json
import argparse
import os.path


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding="utf8") as json_file:
        return json.load(json_file)


def get_biggest_bar(data_from_json ):
    biggest_bar = max(data_from_json, key=lambda bar: bar['Cells']['SeatsCount'])
    return biggest_bar['Cells']['Name']


def get_smallest_bar(data_from_json ):
    smallest_bar = min(data_from_json, key=lambda bar: bar['Cells']['SeatsCount'])
    return smallest_bar['Cells']['Name']


def get_closest_bar(data_from_json , longitude, latitude):
    for bar in data_from_json :
        bar_latitude = bar['Cells']['geoData']['coordinates'][1]
        bar_longitude = bar['Cells']['geoData']['coordinates'][0]
        bar['distance'] = ((latitude - bar_latitude) ** 2 + (longitude - bar_longitude) ** 2) ** 0.5
    closest_bar = min(data_from_json, key= lambda bar: bar['distance'])
    return closest_bar['Cells']['Name']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Данная программа выводит информацию о московских барах на основании данных из файла json')
    args = parser.parse_args()

    while True:
        json_path = input("Укажите путь к существующему файлу json: ")
        data_from_json = load_data(json_path)
        if data_from_json is not None:
            break

    print('Самый большой бар "%s"' % get_biggest_bar(data_from_json )[0])
    print('Самый маленький бар: "%s"' % get_smallest_bar(data_from_json )[0])

    print('Чтобы найти ближайший бар, введите свои координаты:')

    try:
        longitude = float(input("Долгота = "))
        latitude = float(input("Широта = "))
    except ValueError:
        print("Нужно ввести число с точкой в виде разделителя")

    print('Название самого близкого бара: "%s"' % get_closest_bar(data_from_json, longitude, latitude)[0])
