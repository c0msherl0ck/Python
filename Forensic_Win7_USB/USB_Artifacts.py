# -*- coding: utf-8 -*-
import sys
from winreg import *
import re
import requests

def parsingUSBReg(USBinfo_list):
    varSubkey = "SYSTEM\\ControlSet001\\Enum\\USB"  # 서브레지스트리 목록 지정
    varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)  # 루트 레지스트리 핸들 객체 얻기
    varKey = OpenKey(varReg, varSubkey)  # 레지스트리 핸들 객체 얻기

    varKey_len = QueryInfoKey(varKey)[0]
    # print(varKey_len)

    for i in range(1,varKey_len): # ignore the first registry which name is "ROOT_HUB20"
        try:
            keyname = EnumKey(varKey, i)  # 지정한 레지스트리의 하위 키값 조회
            varSubkey2 = "%s\\%s" % (varSubkey, keyname)  # 하위 레지스트리 목록 생성 : 상위 레지스트리 목록과 하위 키값 결합
            # print(varSubkey2)

            regex = re.compile("VID_(.{4})&PID_(.{4})")
            USBinfos = regex.findall(varSubkey2)
            for USBinfo in USBinfos:
                # print("USBinfo : " + str(USBinfo))
                USBinfo_list.append(USBinfo)
        except:
            errorMsg = "Exception", sys.exc_info()[0]
            print(errorMsg)
            break

    CloseKey(varKey)  # 핸들 객체 반환
    CloseKey(varReg)

def makeUSBDictionary(USB_DB, USB_Vendor_DB):
    url = "http://www.linux-usb.org/usb.ids"
    try:
        data = requests.get(url)
    except:
        print("Fail to open the Web Page...")
        exit(-1)
    # make file
    f = open("USBInfoWeb.txt",'w', encoding='utf-8')
    f.write(data.text)
    f.close()
    # read file
    f = open("USBInfoWeb.txt",'r')
    vendor_key = ""
    vendor_value = ""
    product_key = ""
    product_value = ""
    while True:
        line = f.readline()
        if not line:break
        if "# List of known device classes, subclasses and protocols" in line:break
        # print(line)
        regex = re.compile("([a-z0-9]{4})  (.*)")  # two times of spacebar between groups
        match = regex.search(line)
        if match != None :
            if line[0] == '\t': # Product info
                product_key = match.group(1)
                product_value = match.group(2)
                record = [vendor_key,vendor_value,product_key,product_value]
                USB_DB.append(record)
            else: # Vendor info
                vendor_key = match.group(1)
                vendor_value = match.group(2)
                USB_Vendor_DB.append([vendor_key,vendor_value])



    f.close()

if __name__ == "__main__":
    # get USB registry  about Vendor ID and Product ID
    USBinfo_list = [] # list
    parsingUSBReg(USBinfo_list)
    # print(USBinfo_list)

    # get info from  Website and make a USB Database
    USB_DB = [] # Vendor info , Product info
    USB_Vendor_DB = [] # only Vendor info
    makeUSBDictionary(USB_DB, USB_Vendor_DB)

    print("Search with only VID info")
    for record in USB_Vendor_DB:
        for info in USBinfo_list:
            if info[0] in record[0]:
                print(record)
    print("Search with both VID & PID")
    for record in USB_DB:
        for info in USBinfo_list:
            if info[0] in record[0]:
                if info[1] in record[2]:
                    print(record)


