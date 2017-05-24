import json
import sys
import math


def load_data(file_path):
    """ read json data from file and return as list """
    json_object = []
    with open(file_path, 'r', encoding="utf8") as input_data_file:
        json_string = input_data_file.readlines()
    try:
        for i in range(len(json_string)):
            json_object.append(json.loads(json_string[i]))
    except ValueError:
        print("cann't convert json data from file")
        return False
    return json_object


def min_max(function_name, list_data):
    """
    :param function_name: we determine what we whant ti find min or max
    :param list_data: list in which we search min or max
    :return: min or max element and positin of this element in list
    """
    if function_name == "min":
        m = min(list_data)
        minpos = [i + 1 for i, j in enumerate(list_data) if j == m]
        return minpos
    elif function_name == "max":
        m = max(list_data)
        maxpos = [i + 1 for i, j in enumerate(list_data) if j == m]
        return maxpos
    else:
        return None


def get_seats_number(data):
    """
    data - list from json
    list[0] set as "None", because the first number of Bar in json equal 1
    return list as list[k] = v, where  k - Number of bar in json
                                    v - number of seats in bar
    """
    seats = []
    for elem in data:
        seats.append(elem["Cells"]["SeatsCount"])
    return seats


def user_input(desc_string):
    """ Validation of data entry.
    desc_string:  the string describe the input for user
    return: latitude or longitude as float """
    input_data = input(desc_string)
    try:
        input_data = float(input_data)
    except ValueError:
        print("You must specify coordinate")
        print("Script stop work ...")
    return input_data


def get_closest_bar(data, longitude, latitude):
    """ find nearest bar
    :param data: list with info about bars
    :param longitude: coordinate
    :param latitude:  coordinate
    :return: info about nearest bar
    """
    bar_itog_info = []
    list_pos = 0
    min_dist = sys.maxsize
    while list_pos < len(data) - 1:
        info = data[list_pos]['Cells']
        cur_dist = calc_distance(longitude,
                                 latitude,
                                 info['geoData']['coordinates'][0],
                                 info['geoData']['coordinates'][1])
        if cur_dist == min_dist:
            bar_itog_info.append(data[list_pos]['Number'])
        elif cur_dist < min_dist:
            bar_itog_info = list()
            bar_itog_info.append(data[list_pos]['Number'])
            min_dist = cur_dist
        list_pos += 1
    return bar_itog_info


def string_info_about_bar(bar_name, bar_address, bar_adm_area, bar_district,
                          bar_seats_count, bar_dsitance=None):
    """
    return sting info about bar. If distance determine, return
    info string with distance for nearest bar
    """
    if bar_dsitance:
        str_bar_info = "Ближайший бар на расстоянии %.2f метров. " \
                       "Название бара: %s расположен по адресу %s %s %s." \
                       "Имеет %d seats посадочных мест\n" % \
                       (bar_dsitance, bar_name, bar_address,
                        bar_adm_area, bar_district, bar_seats_count)
    else:
        str_bar_info = "Название бара: %s расположен по адресу %s %s %s." \
                       "Имеет %d seats посадочных мест\n" % \
                       (bar_name, bar_address, bar_adm_area,
                        bar_district, bar_seats_count)
    return str_bar_info


def print_data(info_str, bar_numbers, json_string):
    """
    print info about bar
    :param info_str: small info about printing data
    :param bar_numbers: certian bars number in json
    :param json_string: json with info about bars
    :return: none
    """
    print(info_str)
    for i in range(len(bar_numbers)):
        elem = json_string[bar_numbers[i] - 1]['Cells']
        if info_str != "Близкие бары:":
            str_info_bar = string_info_about_bar(elem['Name'],
                                                 elem['Address'],
                                                 elem['AdmArea'],
                                                 elem['District'],
                                                 elem['SeatsCount'])
        else:
            dist = calc_distance(input_longitude,
                                 input_latitude,
                                 elem['geoData']['coordinates'][0],
                                 elem['geoData']['coordinates'][1])
            str_info_bar = string_info_about_bar(elem['Name'],
                                                 elem['Address'],
                                                 elem['AdmArea'],
                                                 elem['District'],
                                                 elem['SeatsCount'],
                                                 dist)
        print(str_info_bar)


def calc_distance(f_a, l_a, f_b, l_b):
    """calculate distance between to points"""
    # calculate how meters in 1 deg latitude
    urm = 6371000 * 2 * math.pi / 360
    # calculate how meters in 1 deg longitude
    urp = math.cos(l_a) * urm
    dist = math.sqrt(
        math.pow((f_b - f_a) * urp, 2) + math.pow((l_b - l_a) * urm, 2))
    return dist


def main_func(json_data, inp_latitude, inp_longitude):
    bars_seats_numbmer = get_seats_number(json_data)
    minpos = min_max("min", bars_seats_numbmer)
    maxpos = min_max("max", bars_seats_numbmer)
    closest_bars = get_closest_bar(json_data, inp_longitude, inp_latitude)

    print_data("Большие бары:", maxpos, json_data)
    print('\n')
    print_data("Маленькие бары:", minpos, json_data)
    print('\n')
    print_data('Близкие бары:', closest_bars, json_data)
    print('\n')


if __name__ == "__main__":
    # if my_environment = "test" we use predefine coordinates
    my_environment = "prod"
    bars_data = list()
    if len(sys.argv) > 1:
        bars_data = load_data(sys.argv[1])
    else:
        print("Please, enter the filepath of data file")
        exit()
    if my_environment != "test":
        input_latitude = user_input('Please, enter latitude:\n')
        input_longitude = user_input('Please, enter longitude:\n')
    else:
        input_latitude = 55.751984
        input_longitude = 37.621128
    print('\n')
    for num in range(len(bars_data)):
        print("Parse the " + str(num) + " json\n")
        main_func(bars_data[num], input_latitude, input_longitude)
