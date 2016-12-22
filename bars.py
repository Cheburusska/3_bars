import json
import argparse
import os.path


def load_data(filepath):
    '''reads data from json file'''
    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding="utf8") as json_file:
        return json.load(json_file)


def get_biggest_bar(data_from_json ):
    '''returns biggest bar'''
    seats = data_from_json [0]['Cells']['SeatsCount']
    bar_name = ''
    for bar in data_from_json :
        if bar['Cells']['SeatsCount'] > seats:
            seats = bar['Cells']['SeatsCount']
            bar_name = bar['Cells']['Name']
    return bar_name, seats


def get_smallest_bar(data_from_json ):
    '''returns smallest bar'''
    seats = data_from_json [0]['Cells']['SeatsCount']
    bar_name = data_from_json [0]['Cells']['Name']
    for bar in data_from_json :
        if bar['Cells']['SeatsCount'] < seats:
            seats = bar['Cells']['SeatsCount']
            bar_name = bar['Cells']['Name']
    return bar_name, seats


def get_closest_bar(data_from_json , longitude, latitude):
    '''returns closest bar'''
    initial_latitude = data_from_json [0]['Cells']['geoData']['coordinates'][1]
    initial_longitude = data_from_json [0]['Cells']['geoData']['coordinates'][0]
    bar_name = data_from_json [0]['Cells']['Name']
    initial_distance = abs(((latitude - initial_latitude) ** 2 + (longitude - initial_longitude) ** 2) ** 0.5)
    for bar in data_from_json :
        bar_latitude = bar['Cells']['geoData']['coordinates'][1]
        bar_longitude = bar['Cells']['geoData']['coordinates'][0]
        bar_distance = ((latitude - bar_latitude) ** 2 + (longitude - bar_longitude) ** 2) ** 0.5
        if bar_distance < initial_distance:
            initial_latitude = bar['Cells']['geoData']['coordinates'][1]
            initial_longitude = bar['Cells']['geoData']['coordinates'][0]
            initial_distance = bar_distance
            bar_name = bar['Cells']['Name']
            address = bar['Cells']['Address']
    return bar_name, initial_latitude, initial_longitude, address


if __name__ == '__main__':
    parser = argparse.ArgumentParser( #help
        description='Данная программа выводит информацию о московских барах на основании данных из файла json')
    args = parser.parse_args()

    while True:
        json_path = input("Укажите путь к существующему файлу json: ")
        data_from_json = load_data(json_path)
        if data_from_json is not None:
            break

    print('Название самого большого бара: "%s"' % get_biggest_bar(data_from_json )[0])
    print('Количество мест в нем: %s' % get_biggest_bar(data_from_json )[1])

    print('Название самого маленького бара: "%s"' % get_smallest_bar(data_from_json )[0])
    print('Количество мест в нем: %s' % get_smallest_bar(data_from_json )[1])

    while True:
        print('Чтобы найти ближайший бар, введите свои координаты:')
        longitude = input("Долгота = ")
        latitude = input("Широта = ")
        if longitude.isdigit() == True and latitude.isdigit() == True:
            longitude = float(longitude)
            latitude = float(latitude)
            print('Название самого близкого бара: "%s"' % get_closest_bar(data_from_json , longitude, latitude)[0])
            print('Его координаты: широта %s, долгота %s' % (get_closest_bar(data_from_json , longitude, latitude)[1],
                  get_closest_bar(data_from_json , longitude, latitude)[2]))
            print('Адрес: %s' % get_closest_bar(data_from_json , longitude, latitude)[3])
            break
        else:
            print("Необходимо вводить только числа")
