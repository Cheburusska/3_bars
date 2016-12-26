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
    return biggest_bar['Cells']['Name'], biggest_bar['Cells']['SeatsCount']


def get_smallest_bar(data_from_json ):
    smallest_bar = min(data_from_json, key=lambda bar: bar['Cells']['SeatsCount'])
    return smallest_bar['Cells']['Name'], smallest_bar['Cells']['SeatsCount']


def get_closest_bar(data_from_json , longitude, latitude):
    for bar in data_from_json :
        bar_latitude = bar['Cells']['geoData']['coordinates'][1]
        bar_longitude = bar['Cells']['geoData']['coordinates'][0]
        bar['distance'] = ((latitude - bar_latitude) ** 2 + (longitude - bar_longitude) ** 2) ** 0.5
    closest_bar = min(data_from_json, key= lambda bar: bar['distance'])
    return closest_bar['Cells']['Name'], closest_bar['Cells']['geoData']['coordinates'][1], closest_bar['Cells']['geoData']['coordinates'][0], closest_bar['Cells']['Address']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Данная программа выводит информацию о московских барах на основании данных из файла json')
    args = parser.parse_args()

    
    while True:
        json_path = input("Укажите путь к существующему файлу json: ")
        data_from_json = load_data(json_path)
        if data_from_json is not None:
            break

    print('Самый большой бар "%s", мест %s' % (get_biggest_bar(data_from_json )[0], get_biggest_bar(data_from_json )[1]))
    print('Самый маленький бар: "%s", мест %s' % (get_smallest_bar(data_from_json )[0], get_smallest_bar(data_from_json )[1]))

    print('Чтобы найти ближайший бар, введите свои координаты:')
    while True:
        try:
            longitude = float(input("Долгота = "))
            latitude = float(input("Широта = "))
            break
        except ValueError:
            print ("Нужно ввести число с точкой в виде разделителя")

    print('Название самого близкого бара: "%s"' % get_closest_bar(data_from_json, longitude, latitude)[0])
    print('Его координаты: широта %s, долгота %s' % (get_closest_bar(data_from_json, longitude, latitude)[1],
                                                     get_closest_bar(data_from_json, longitude, latitude)[2]))
    print('Адрес: %s' % get_closest_bar(data_from_json, longitude, latitude)[3])
