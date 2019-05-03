import os
import re
from bs4 import BeautifulSoup
import sqlite3

def parseFromCert(dirname, DB):
    # [ip, username, account, bank, country]
    regex = re.compile("cn=(.*)\(\)([\d]*),ou=(.*),ou=personal,o=yessign,c=(.*)")
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        full_filename = full_filename + "/signCert.cert"
        # print(full_filename)
        f = open(full_filename, encoding="CP949", mode="r")
        data = f.read()
        # print(data)
        match = regex.match(data)
        if match:
            record = [filename, match.group(1), match.group(2), match.group(3), match.group(4)]
            # print(record)
            DB.append(record)
        else:
            print("No match")

def parseFromWeb(webpage, DB):
    f = open(webpage,"r")
    data = f.read()
    soup = BeautifulSoup(data, "lxml")
    f.close()
    trList = soup.select("tr")

    regex_ip = re.compile("([\d]+.[\d]+.[\d]+.[\d]+)")
    regex_time = re.compile("([\d]+-[\d]+-[\d]+[\s][\d]+:[\d]+)")

    for tr in trList:
        tdList = tr.select("td")
        if len(tdList) == 5:
            if tdList[1].select_one("a") is not None:
                ip = tdList[1].select_one("a").text
                time = tdList[2].text
                match_ip = regex_ip.search(ip)
                match_time = regex_time.search(time)
                if match_ip is not None:
                    # print(match_ip.group(1))
                    # print(match_time.group(1))
                    # DB.append([match_ip.group(1), match_time.group(1)])
                    DB[match_ip.group(1)] = match_time.group(1)

def integratingDB(CertDB, WebDB, integratedDB):
    for certdb in CertDB:
        record = [certdb[0], WebDB[certdb[0]], certdb[1], certdb[3], certdb[2], certdb[4]]
        integratedDB.append(record)

def pushToSQLDB(integratedDB):
    conn = sqlite3.connect("integrated.db")
    cur = conn.cursor()
    sql = "create table victim (ip, time, username, bank, account, country)"
    cur.execute(sql)
    for row in integratedDB:
        sql = "insert into victim (ip, time, username, bank, account, country) values (?, ?, ?, ?, ?, ?)"
        cur.execute(sql,(row[0], row[1], row[2], row[3], row[4], row[5]))
    conn.commit()
    conn.close()

# [ip, username, account, bank, country]
CertDB = []
parseFromCert("unzipCertSet", CertDB)
print(CertDB)
# [ip, modified time]
webpage = "webpageTxt"
WebDB = {}
parseFromWeb(webpage, WebDB)
print(WebDB)
# [ip, modified time, username, bank, account, country]  ip is the key
integratedDB = []
integratingDB(CertDB, WebDB, integratedDB)
print(integratedDB)

pushToSQLDB(integratedDB)