# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# https://github.com/charlierguo/gmail
# pip support not yet implemented
# interpreter : python 2.7
import gmail
import hashlib
import os
import re
import requests
import urllib
import urllib2
import httplib
import exifread # extract gps data from image
import unicodedata # NFD to NFC
from gmplot import gmplot # gmaps

# based on https://gist.github.com/erans/983821
def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)

def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat
        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon
    return lat, lon
# end of the exif extracting and calculating GPS info

def getCurrentDirPath():
    # get the current directory of the code file existed
    pwdPath = os.path.dirname(os.path.realpath(__file__))
    return pwdPath

def checkAndDownload(shortendURL, realURL, mailDate, mailDateTime):
    # decode part
    realURLStr = urllib2.unquote(realURL).decode("utf-8") # URL Decode
    realURLStr = unicodedata.normalize('NFC', realURLStr) # NFD to NFC
    # check if it is comprised of 'fl0ckfl0ck.info/'
    if realURLStr.find("http://fl0ckfl0ck.info/") != -1:
        # get the name of the image file
        img_name = realURLStr.replace("http://fl0ckfl0ck.info/","")
        # download the image
        urllib.urlretrieve(realURL, getCurrentDirPath() +"\\"+ mailDate +"\\"+ img_name)
        print("download is completed")
        # calculate the hash value of the image file
        f = open(getCurrentDirPath() +"\\"+ mailDate +"\\"+ img_name, 'rb')
        data = f.read()
        f.close()
        # get the GPS info from image file
        f = open(getCurrentDirPath() + "\\" + mailDate + "\\" + img_name, 'rb')
        tags = exifread.process_file(f)
        gps = get_exif_location(tags)
        if gps[0] == None or gps[1] == None:
            lat = "0"
            lon = "0"
        else:
            lat = "%0.6f" % gps[0]
            lon = "%0.6f" % gps[1]
        f.close()
        # open the result.csv file and record
        row = mailDateTime+"\t"+shortendURL+"\t"+realURLStr+"\t"+img_name+"\t"+lat+"\t"+lon+"\t"+hashlib.md5(data).hexdigest()+"\t"+hashlib.sha1(data).hexdigest()+"\n"
        f = open(getCurrentDirPath() +"\\"+ mailDate +"\\"+'result.csv', 'ab+')
        f.write(row)
        f.close()
        print("writing the image info is completed")
    else:
        print("there is no fl0ckfl0ck")

def URLAuthenticating(matchURL, mailDate, mailDateTime):
    # print("matchURL length : "+str(len(matchURL)))
    cnt = 0
    index = 0
    # find the index of third '/' from url
    for i in range(0,len(matchURL)):
        if matchURL[i] == '/':
            cnt = cnt + 1
        if cnt == 3:
            index = i
            break
    # authenticate url by characters
    # if the url response status code is 200, and if it is comprised of 'fl0ckfl0ck.info', then download the image
    for i in range(index+2, len(matchURL)+1):
        testURL = matchURL[0:i]
        try:
            response = requests.get(testURL)
            if response.status_code == 200:
                try:
                    realURL = urllib2.urlopen(testURL)
                    realURL = realURL.url
                    print("the real URL : "+realURL+"   status : "+str(response.status_code))
                    checkAndDownload(testURL, realURL, mailDate, mailDateTime)
                except urllib2.HTTPError as e:
                    print("HTTPError")
                    continue
                except urllib2.URLError as e:
                    print("URLError")
                    continue
                except httplib.HTTPException as e:
                    print("HTTPException")
                    continue
        except requests.exceptions.RequestException as e:
            # print(e)
            print("RequestException")
            continue


# this is a main function
if __name__ == "__main__":
    # parsing from gmail
    username = "user@gmail.com"
    password = "password"
    try:
        g = gmail.login(username, password)
        print('login success')
        # parse the unread mails from fl0ckfl0ck
        unreads = g.inbox().mail(unread=True, sender="fl0ckfl0ck@hotmail.com")
        # unreads = g.inbox().mail(sender="fl0ckfl0ck@hotmail.com")  # if you want to read all emails from fl0ckfl0ck
        for unread in unreads:
            print("=======================================================================================================")
            # read the content, date, time of mail
            unread.fetch()
            mailDateTime = str(unread.sent_at)  # time of mail
            mailDateSplited = mailDateTime.split(" ")
            mailDate = mailDateSplited[0] # date of mail
            print(mailDateTime)
            print(unread.body)
            # mark as read
            unread.read()
            # make directory which name is YYYY-MM-DD, If it does not exist
            if not os.path.isdir(getCurrentDirPath() + "\\" + mailDate):
                os.mkdir(getCurrentDirPath() + "\\" + mailDate)

            # make the result.csv file
            f = open(getCurrentDirPath() + "\\" + mailDate + "\\" + 'result.csv', 'ab+')
            f.close()

            # find all patterns satisfying the regular expression below
            # http[s]?://\w+[.]\w+/\w+
            regex = re.compile("http[s]?://\w+[.]\w+/\w+")
            matchURLs = regex.findall(unread.body)
            for matchURL in matchURLs:
                print("matchURL : "+str(matchURL))
                URLAuthenticating(matchURL, mailDate, mailDateTime)
        g.logout()
    except gmail.AuthenticationError:
        print('login failed : AuthenticationError')

    # make the integratedDB.csv
    cPath = getCurrentDirPath()
    # initialize the integratedDB.csv
    f2 = open(cPath + "\\" + 'integratedDB.csv', 'wb+')
    f2.close()
    # read all result.csv files from each directories
    regex = re.compile("2018[-]08[-]\d\d")
    for name in os.listdir(cPath):
        if regex.search(name) != None:
            if os.path.isdir(cPath + "\\" + name):
                f = open(cPath + "\\" + name + "\\" + 'result.csv', 'rb')
                data = f.read()
                f2 = open(cPath + "\\" + 'integratedDB.csv', 'ab+')
                f2.write(data)
                f2.close()
                f.close()

    # draw a picture based on GPS from integrated DB
    # get GPS info
    gpsList = []
    cPath = getCurrentDirPath()
    f = open(cPath + "\\" + 'integratedDB.csv', 'rb')
    bundleOfData = f.readlines()
    for data in bundleOfData:
        data = data.split('\t')
        if (float(data[4]) != 0) and (float(data[5]) != 0): # filtering '0'
            gpsList.append((float(data[4]), float(data[5]), data[3]))  # latitude, longtitude, img_name
    f.close()

    lats = []
    lons = []
    for gps in gpsList:
        print(gps[0], gps[1])
        lats.append(gps[0])
        lons.append(gps[1])

    # Place map
    gmap = gmplot.GoogleMapPlotter(gpsList[0][0], gpsList[0][1], 9)
    # draw lines
    gmap.plot(lats, lons, 'red', edge_width=5)
    # drop pins
    cnt = 1
    for x,y in zip(lats, lons):
        gmap.marker(x,y, 'cornflowerblue', title=cnt)
        cnt = cnt+1
    # Draw
    gmap.draw("result_map.html")