import csv
import os
from collections import OrderedDict


def _returnRanking():
    """
    Countでソートされた辞書のリストを返す関数
    """
    with open('ranking.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        notSortedDict = {}
        for row in reader:
            notSortedDict[row['Name']] = int(row['Count'])
    ranking = sorted(notSortedDict.items(),
                     key=lambda x: x[1], reverse=True)
    return ranking


def _updateCsv(restaurantName):
    """
    1. CSVを開く
    2. ユーザーが入力したレストラン名を探す
    3. レストラン名を入力と照合
    4. 照合した場合、そのindex番号のdictを取得、countを+1して更新
    5. 照合し、なかった場合、末尾にデフォルト値を追加
    """
    restaurantName = restaurantName.title()
    with open('ranking.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        dictList = [row for row in reader]
        if restaurantName in [row['Name'] for row in dictList]:
            for i, restaurantDict in enumerate(dictList):
                if restaurantName == restaurantDict['Name']:
                    dictList[i]['Count'] = int(dictList[i]['Count']) + 1
        else:
            dictList.append(OrderedDict(
                {'Name': restaurantName, 'Count': 1}))
        with open('ranking.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['Name', 'Count'])
            writer.writeheader()
            writer.writerows(dictList)


def greeting():
    while True:
        personName = input(
            'こんにちは!私はRobokoです。あなたの名前は何ですか?\n'
        )
        if os.path.exists('ranking.csv'):
            restaurantsList = _returnRanking()
            for restaurant in restaurantsList:
                answer = input(
                    f"私のオススメのレストランは、{restaurant[0]}です。このレストランは好きですか？\n")
                if answer.lower() == 'yes':
                    break
        restaurantName = input(f'{personName}さん。どこのレストランが好きですか？\n')
        print(f'{personName}さん。ありがとうございました。良い1日を！さようなら')
        _updateCsv(restaurantName)
        break
