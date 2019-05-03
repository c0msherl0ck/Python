# -*- coding: utf-8 -*-
import sys
import requests
import lxml
from bs4 import BeautifulSoup
import pandas
import openpyxl

def crawling_and_calculating(url):
    # df_2 for February 2019.02.01 ~ 2019.02.28
    # df_3 for March 2019.03.01 ~ 2019.03.31
    df_2 = pandas.DataFrame()
    df_3 = pandas.DataFrame()
    # February
    for i in range(1,29):
        sdate_param = '2019.02.'+str(i).zfill(2)
        print(sdate_param)
        params = {'area': '전체 지역', 'area-2': '전체 회원권', 'sdate': sdate_param, 'edate': 'undefined', 'gsort': '1'}
        try:
            r = requests.post(url, data=params)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        soup = BeautifulSoup(r.content, 'lxml')
        trList = soup.select('tr')
        row = {}
        for tr in trList:
            tdList = tr.select('td')
            # print(len(tdList))
            if len(tdList) == 6:
                row[tdList[0].text] = int(tdList[1].text.replace(',',''))
        df_2_row = pandas.DataFrame(row, index=[i-1])
        df_2 = df_2.append(df_2_row, sort=False)
    # March
    for i in range(1,32):
        sdate_param = '2019.03.'+str(i).zfill(2)
        print(sdate_param)
        params = {'area': '전체 지역', 'area-2': '전체 회원권', 'sdate': sdate_param, 'edate': 'undefined', 'gsort': '1'}
        try:
            r = requests.post(url, data=params)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        soup = BeautifulSoup(r.content, 'lxml')
        trList = soup.select('tr')
        row = {}
        for tr in trList:
            tdList = tr.select('td')
            # print(len(tdList))
            if len(tdList) == 6:
                row[tdList[0].text] = int(tdList[1].text.replace(',',''))
        df_3_row = pandas.DataFrame(row, index=[i-1])
        df_3 = df_3.append(df_3_row, sort=False)

    print(df_2.index)
    print(df_2.columns)
    print(df_2.mean())

    print(df_3.index)
    print(df_3.columns)
    print(df_3.mean())

    df_mean = pandas.DataFrame()
    df_mean = df_mean.append(df_2.mean(), sort=False, ignore_index=True)
    df_mean = df_mean.append(df_3.mean(), sort=False, ignore_index=True)
    print(df_mean.head())
    df_excel = df_mean.T # Reversing columns and rows
    df_excel.rename(columns={0:'Febraury', 1:'March'}, inplace=True) # Rename columns
    print(df_excel.head())
    return df_excel

if __name__ == '__main__':
    url_golf = 'http://www.dongagolf.co.kr/inc/sise/sise_price_GM_blist.php'
    url_condo = 'http://www.dongagolf.co.kr/inc/sise/sise_price_CM_blist.php'
    url_fitness = 'http://www.dongagolf.co.kr/inc/sise/sise_price_SM_blist.php'
    # Crawling data from website, calculate the means by month
    df_golf = crawling_and_calculating(url_golf)
    df_condo = crawling_and_calculating(url_condo)
    df_fitness = crawling_and_calculating(url_fitness)
    # Create a Excel file, Write a value to excel
    with pandas.ExcelWriter('output.xlsx') as writer:
        df_golf.to_excel(writer, sheet_name='golf')
        df_condo.to_excel(writer, sheet_name='condo')
        df_fitness.to_excel(writer, sheet_name='fitness')
    # Write a column name to A1 cell at each of the sheets
    book = openpyxl.load_workbook('output.xlsx')
    sheet_golf = book.get_sheet_by_name('golf')
    sheet_condo = book.get_sheet_by_name('condo')
    sheet_fitness = book.get_sheet_by_name('fitness')
    sheet_golf['A1'] = '회원권명'
    sheet_condo['A1'] = '회원권명'
    sheet_fitness['A1'] = '회원권명'
    book.save('output.xlsx')