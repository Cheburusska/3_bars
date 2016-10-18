import json

json_path = 'bars.json'


def load_data(filepath):
    with open(filepath, encoding="utf8") as json_file:
        data = json.load(json_file)
        return data


def get_biggest_bar(data):
    seats = data[0]['Cells']['SeatsCount']
    name = ''
    for bar in data:
        if bar['Cells']['SeatsCount'] > seats:
            seats = bar['Cells']['SeatsCount']
            name = bar['Cells']['Name']
    print('Название самого большого бара: "%s"' % name)
    print('Количество мест в нем: %s' % seats)


def get_smallest_bar(data):
    seats = data[0]['Cells']['SeatsCount']
    name = data[0]['Cells']['Name']
    for bar in data:
        if bar['Cells']['SeatsCount'] < seats:
            seats = bar['Cells']['SeatsCount']
            name = bar['Cells']['Name']
    print('Название самого маленького бара: "%s"' % name)
    print('Количество мест в нем: %s' % seats)


def get_closest_bar(data, longitude, latitude):
    x = data[0]['Cells']['geoData']['coordinates'][1]
    y = data[0]['Cells']['geoData']['coordinates'][0]
    name = data[0]['Cells']['Name']
    r = abs(((latitude - x) ** 2 + (longitude - y) ** 2) ** 0.5)
    for bar in data:
        x2 = bar['Cells']['geoData']['coordinates'][1]
        y2 = bar['Cells']['geoData']['coordinates'][0]
        r2 = ((latitude - x2) ** 2 + (longitude - y2) ** 2) ** 0.5
        if r2  < r:
            x = bar['Cells']['geoData']['coordinates'][1]
            y = bar['Cells']['geoData']['coordinates'][0]
            r = r2
            name = bar['Cells']['Name']
            addr = bar['Cells']['Address']
    print('Название самого близкого бара: "%s"' % name)
    print('Его координаты: широта %s, долгота %s' % (x,y))
    print('адрес: {}'.format(addr))


if __name__ == '__main__':
    data = load_data(json_path)
    get_biggest_bar(data)
    get_smallest_bar(data)
    while True:
        print ('Чтобы найти ближайший бар, введите свои координаты:')
        longitude = input("Долгота = ")
        latitude = input("Широта = ")
        if longitude.isdigit() == True and latitude.isdigit() == True:
            longitude = float(longitude)
            latitude = float (latitude)
            get_closest_bar(data, longitude, latitude)
            break
        else:
            print ("Необходимо вводить только числа")
