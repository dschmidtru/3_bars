import json
import sys
import math


def load_data(filepath):
    """
    Read json from file
    :param filepath: Filepath of data file
    :return: data from file as list
    """
    with open(filepath, 'r', encoding="utf8") as input_data_file:
        json_string = input_data_file.readline()
    input_data_file.close()
    try:
        json_data = json.loads(json_string)
        return json_data
    except ValueError:
        print("cann't convert json data from file")
        exit()


def get_biggest_bar(data):
    biggest_bar = {'Address': '', 'AdmArea': '', 'District': '', 'Name': '',
                   'SeatsCount': 0}
    bar_itog_info = []
    for cur_bar_data in data:
        cur_bar_data = cur_bar_data['Cells']
        if cur_bar_data['SeatsCount'] == biggest_bar['SeatsCount']:
            biggest_bar['Address'] = cur_bar_data['Address']
            biggest_bar['AdmArea'] = cur_bar_data['AdmArea']
            biggest_bar['District'] = cur_bar_data['District']
            biggest_bar['Name'] = cur_bar_data['Name']
            biggest_bar['SeatsCount'] = cur_bar_data['SeatsCount']
            bar_itog_info.append(biggest_bar)
        if cur_bar_data['SeatsCount'] > biggest_bar['SeatsCount']:
            bar_itog_info = []
            biggest_bar['Address'] = cur_bar_data['Address']
            biggest_bar['AdmArea'] = cur_bar_data['AdmArea']
            biggest_bar['District'] = cur_bar_data['District']
            biggest_bar['Name'] = cur_bar_data['Name']
            biggest_bar['SeatsCount'] = cur_bar_data['SeatsCount']
            bar_itog_info.append(biggest_bar)
    return bar_itog_info


def get_smallest_bar(data):
    smallest_bar = {'Address': '', 'AdmArea': '', 'District': '', 'Name': '',
                    'SeatsCount': sys.maxsize}
    bar_itog_info = []
    for cur_bar_data in data:
        cur_bar_data = cur_bar_data['Cells']
        if cur_bar_data['SeatsCount'] == smallest_bar['SeatsCount']:
            smallest_bar = {'Address': cur_bar_data['Address'],
                            'AdmArea': cur_bar_data['AdmArea'],
                            'District': cur_bar_data['District'],
                            'Name': cur_bar_data['Name'],
                            'SeatsCount': cur_bar_data['SeatsCount']}
            bar_itog_info.append(smallest_bar)
        if cur_bar_data['SeatsCount'] < smallest_bar['SeatsCount']:
            bar_itog_info = []
            smallest_bar['Address'] = cur_bar_data['Address']
            smallest_bar['AdmArea'] = cur_bar_data['AdmArea']
            smallest_bar['District'] = cur_bar_data['District']
            smallest_bar['Name'] = cur_bar_data['Name']
            smallest_bar['SeatsCount'] = cur_bar_data['SeatsCount']
            bar_itog_info.append(smallest_bar)
    return bar_itog_info


def calc_distance(f_a, l_a, f_b, l_b):
    """
    :param f_a: longitude of A point
    :param l_a: latitude of A point
    :param f_b: longitude of B point
    :param l_b: latitude of B point
    :return: distance bitween two point on map
    description of algorithm can be found here:
    http://gis-lab.info/qa/great-circles.html
    """

    earth_radius = 6372795

    lat1 = f_a * math.pi / 180
    lat2 = f_b * math.pi / 180
    long1 = l_a * math.pi / 180
    long2 = l_b * math.pi / 180

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 *
                                                       cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta

    ad = math.atan2(y, x)
    dist = ad * earth_radius

    return dist


def get_closest_bar(data, longitude, latitude):
    closest_bar = {'Address': '', 'AdmArea': '', 'District': '', 'Name': '',
                   'SeatsCount': 0, 'longitude': 0, 'latitude': 0}
    bar_itog_info = []
    num = 0
    min_dist = 0
    while num < (len(data)) - 1:
        if num == 0:
            info = data[num]['Cells']
            closest_bar = {'Address': info['Address'],
                           'AdmArea': info['AdmArea'],
                           'District': info['District'],
                           'Name': info['Name'],
                           'SeatsCount': info['SeatsCount'],
                           'longitude': info['geoData']['coordinates'][0],
                           'latitude': info['geoData']['coordinates'][1]}
            min_dist = calc_distance(longitude, latitude,
                                     closest_bar['longitude'],
                                     closest_bar['latitude'])
            closest_bar['distance'] = min_dist
            bar_itog_info.append(closest_bar)
        else:
            info = data[num]['Cells']
            dist = calc_distance(longitude, latitude,
                                 info['geoData']['coordinates'][0],
                                 info['geoData']['coordinates'][1])
            if dist == min_dist:
                info = data[num]['Cells']
                closest_bar = {'Address': info['Address'],
                               'AdmArea': info['AdmArea'],
                               'District': info['District'],
                               'Name': info['Name'],
                               'SeatsCount': info['SeatsCount'],
                               'longitude': info['geoData']['coordinates'][0],
                               'latitude': info['geoData']['coordinates'][1],
                               'distance': dist}
                bar_itog_info.append(closest_bar)
            elif dist < min_dist:
                bar_itog_info = []
                info = data[num]['Cells']
                closest_bar['Address'] = info['Address']
                closest_bar['AdmArea'] = info['AdmArea']
                closest_bar['District'] = info['District']
                closest_bar['Name'] = info['Name']
                closest_bar['SeatsCount'] = info['SeatsCount']
                closest_bar['longitude'] = info['geoData']['coordinates'][0]
                closest_bar['latitude'] = info['geoData']['coordinates'][1]
                closest_bar['distance'] = dist
                bar_itog_info.append(closest_bar)
        num = num + 1
    return bar_itog_info


def printing_data(info_str, data):
    print(info_str)
    if len(data) > 1:
        for elem in data:
            if 'distance' in data[0]:
                strp = "Ближайший бар на расстоянии %.2f метров. " \
                       "Название бара: %s расположен по адресу %s %s %s." \
                       "Имеет %d seats посадочных мест\n" % \
                       (elem['distance'], elem['Name'], elem['Address'],
                        elem['AdmArea'], elem['District'], elem['SeatsCount'])
                print(strp)
            else:
                strp = "Название бара: %s расположен по адресу %s %s %s." \
                       "Имеет %d seats посадочных мест\n" % \
                       (elem['Name'], elem['Address'], elem['AdmArea'],
                        elem['District'], elem['SeatsCount'])
                print(strp)
    else:
        print('')
        if 'distance' in data[0]:
            strp = "Ближайший бар на расстоянии %.2f метров. " \
                   "Название бара: %s расположен по адресу %s %s %s." \
                   "Имеет %d seats посадочных мест\n" % \
                   (data[0]['distance'], data[0]['Name'], data[0]['Address'],
                    data[0]['AdmArea'], data[0]['District'],
                    data[0]['SeatsCount'])
            print(strp)

        else:
            strp = "Название бара: %s расположен по адресу %s %s %s." \
                   " Имеет %d seats посадочных мест\n" % \
                   (data[0]['Name'], data[0]['Address'], data[0]['AdmArea'],
                    data[0]['District'], data[0]['SeatsCount'])
            print(strp)


def user_input(desc_string):
    """
    Validation of data entry
    :param desc_string:  the string describe the input
    :return: latitude or longitude as float
    """
    check_input = True
    input_data = ""
    while check_input:
        input_data = input(desc_string)
        try:
            input_data = float(input_data)
            check_input = False
        except ValueError:
            print("You must specify coordinate")
    return input_data


if __name__ == '__main__':
    bars_data = ""
    if len(sys.argv) > 1:
        bars_data = load_data(sys.argv[1])
    else:
        print("Please, enter the filepath of data file")
        exit()
    input_latitude = user_input('Please, enter latitude:\n')
    input_longitude = user_input('Please, enter longitude:\n')
    print('\n')
    biggest_bars = get_biggest_bar(bars_data)
    printing_data('Большие бары:', biggest_bars)
    print('\n')
    smallest_bars = get_smallest_bar(bars_data)
    printing_data('Маленькие бары:', smallest_bars)
    print('\n')
    closest_bars = get_closest_bar(bars_data, input_longitude, input_latitude)
    printing_data('Близкие бары:', closest_bars)
