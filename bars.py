# -*- coding: utf-8 -*-
import json
import sys
import math


def load_data(filepath):
    json_string = open(filepath, 'r', encoding="utf8").readline()
    return json.loads(json_string)


def get_biggest_bar(data):
    biggestBar = {'Address': '', 'AdmArea': '', 'District': '', 'Name': '', 'SeatsCount': 0}
    barItogInfo = []
    for curBarData in (data):
        curBarData = curBarData['Cells']
        if curBarData['SeatsCount'] == biggestBar['SeatsCount']:
            smallestBar = {}
            biggestBar['Address'] = curBarData['Address']
            biggestBar['AdmArea'] = curBarData['AdmArea']
            biggestBar['District'] = curBarData['District']
            biggestBar['Name'] = curBarData['Name']
            biggestBar['SeatsCount'] = curBarData['SeatsCount']
            barItogInfo.append(biggestBar)
        if curBarData['SeatsCount'] > biggestBar['SeatsCount']:
            barItogInfo = []
            biggestBar['Address'] = curBarData['Address']
            biggestBar['AdmArea'] = curBarData['AdmArea']
            biggestBar['District'] = curBarData['District']
            biggestBar['Name'] = curBarData['Name']
            biggestBar['SeatsCount'] = curBarData['SeatsCount']
            barItogInfo.append(biggestBar)
    return barItogInfo


def get_smallest_bar(data):
    smallestBar = {'Address': '', 'AdmArea': '', 'District': '', 'Name': '', 'SeatsCount': sys.maxsize}
    barItogInfo = []
    for curBarData in (data):
        curBarData = curBarData['Cells']
        if curBarData['SeatsCount'] == smallestBar['SeatsCount']:
            smallestBar = {}
            smallestBar['Address'] = curBarData['Address']
            smallestBar['AdmArea'] = curBarData['AdmArea']
            smallestBar['District'] = curBarData['District']
            smallestBar['Name'] = curBarData['Name']
            smallestBar['SeatsCount'] = curBarData['SeatsCount']
            barItogInfo.append(smallestBar)
        if curBarData['SeatsCount'] < smallestBar['SeatsCount']:
            barItogInfo = []
            smallestBar['Address'] = curBarData['Address']
            smallestBar['AdmArea'] = curBarData['AdmArea']
            smallestBar['District'] = curBarData['District']
            smallestBar['Name'] = curBarData['Name']
            smallestBar['SeatsCount'] = curBarData['SeatsCount']
            barItogInfo.append(smallestBar)
    return barItogInfo


def calcDistance(fA, lA, fB, lB):
    earthRadius = 6372795

    lat1 = fA * math.pi / 180
    lat2 = fB * math.pi / 180
    long1 = lA * math.pi / 180
    long2 = lB * math.pi / 180

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta

    ad = math.atan2(y, x)
    dist = ad * earthRadius

    return dist


def get_closest_bar(data, longitude, latitude):
    closestBar = {'Address': '', 'AdmArea': '', 'District': '', 'Name': '', 'SeatsCount': 0, 'longitude': 0,
                  'latitude': 0}
    barItogInfo = []
    num = 0
    minDist = 0
    while num < (len(data)) - 1:
        if num == 0:
            closestBar = {}
            closestBar['Address'] = data[num]['Cells']['Address']
            closestBar['AdmArea'] = data[num]['Cells']['AdmArea']
            closestBar['District'] = data[num]['Cells']['District']
            closestBar['Name'] = data[num]['Cells']['Name']
            closestBar['SeatsCount'] = data[num]['Cells']['SeatsCount']
            closestBar['longitude'] = data[num]['Cells']['geoData']['coordinates'][0]
            closestBar['latitude'] = data[num]['Cells']['geoData']['coordinates'][1]
            minDist = calcDistance(longitude, latitude, closestBar['longitude'], closestBar['latitude'])
            closestBar['distance'] = minDist
            barItogInfo.append(closestBar)
        else:
            dist = calcDistance(longitude, latitude, data[num]['Cells']['geoData']['coordinates'][0],
                                data[num]['Cells']['geoData']['coordinates'][1])
            if dist == minDist:
                closestBar = {}
                closestBar['Address'] = data[num]['Cells']['Address']
                closestBar['AdmArea'] = data[num]['Cells']['AdmArea']
                closestBar['District'] = data[num]['Cells']['District']
                closestBar['Name'] = data[num]['Cells']['Name']
                closestBar['SeatsCount'] = data[num]['Cells']['SeatsCount']
                closestBar['longitude'] = data[num]['Cells']['geoData']['coordinates'][0]
                closestBar['latitude'] = data[num]['Cells']['geoData']['coordinates'][1]
                closestBar['distance'] = dist
                barItogInfo.append(closestBar)
            elif dist < minDist:
                barItogInfo = []
                closestBar['Address'] = data[num]['Cells']['Address']
                closestBar['AdmArea'] = data[num]['Cells']['AdmArea']
                closestBar['District'] = data[num]['Cells']['District']
                closestBar['Name'] = data[num]['Cells']['Name']
                closestBar['SeatsCount'] = data[num]['Cells']['SeatsCount']
                closestBar['longitude'] = data[num]['Cells']['geoData']['coordinates'][0]
                closestBar['latitude'] = data[num]['Cells']['geoData']['coordinates'][1]
                closestBar['distance'] = dist
                barItogInfo.append(closestBar)
        num = num + 1
    return barItogInfo


def printingData(str, data):
    print(str)
    if len(data) > 1:
        for dict in data:
            if 'distance' in data[0]:
                strp = "Ближайший бар на расстоянии %.2f метров. Название бара: %s расположен по адресу %s %s %s. Имеет %d seats посадочных мест\n" % (
                dict['distance'], dict['Name'], dict['Address'], dict['AdmArea'], dict['District'], dict['SeatsCount'])
                print(strp)
            else:
                strp = "Название бара: %s расположен по адресу %s %s %s. Имеет %d seats посадочных мест\n" % (
                dict['Name'], dict['Address'], dict['AdmArea'], dict['District'], dict['SeatsCount'])
                print(strp)
    else:
        print('')
        if 'distance' in data[0]:
            strp = "Ближайший бар на расстоянии %.2f метров. Название бара: %s расположен по адресу %s %s %s. Имеет %d seats посадочных мест\n" % (
            data[0]['distance'], data[0]['Name'], data[0]['Address'], data[0]['AdmArea'], data[0]['District'],
            data[0]['SeatsCount'])
            print(strp)
        else:
            strp = "Название бара: %s расположен по адресу %s %s %s. Имеет %d seats посадочных мест\n" % (
            data[0]['Name'], data[0]['Address'], data[0]['AdmArea'], data[0]['District'], data[0]['SeatsCount'])
            print(strp)


if __name__ == '__main__':
    barsdata = load_data('Бары.json')
    # latitude = (float(input('Please, enter latitude:\n')))
    # longitude = (float(input('Please, enter longitude:\n')))
    latitude = 55.752705
    longitude = 37.622731
    print('\n')
    biggestBars = get_biggest_bar(barsdata)
    printingData('Большие бары:', biggestBars)
    print('\n')
    smallestBars = get_smallest_bar(barsdata)
    printingData('Маленькие бары:', smallestBars)
    print('\n')
    closestBars = get_closest_bar(barsdata, longitude, latitude)
    printingData('Близкие бары:', closestBars)
