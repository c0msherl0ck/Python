import os
import sys
import time
import pefile
import hashlib
import pprint
from datetime import datetime, timezone

def main(string):
    print('The directory path to search : '+string)

# https://wikidocs.net/39
def search(dirname, pefilePathList):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename, pefilePathList) # recursive function
            else:
                ext = os.path.splitext(full_filename)[-1]
                # check that the file is PE (Portable Execution)
                if ext == '.exe' or ext == '.scr' or ext == '.dll' or ext == '.ocx' or ext == '.cpl' or ext == '.drv' or ext == '.sys' or ext == '.vxd' or ext == '.obj':
                    # print(full_filename)
                    pefilePathList.append(full_filename)
    except PermissionError:
        pass

def printPEInfo(pefilePathList):
    for pefilePath in pefilePathList:
        # pefile path
        print(pefilePath)

        f = open(pefilePath, 'rb')
        data = f.read()
        print("File MD5 : " + hashlib.md5(data).hexdigest())
        f.close()
        # print("File creation time : "+str(time.ctime(os.path.getctime(pefilePath))))

        # pefile 객체 생성
        pe = pefile.PE(pefilePath)
        # compilation time 추출
        # pprint.pprint(dir(pe.FILE_HEADER))
        utc_time = datetime.fromtimestamp(pe.FILE_HEADER.TimeDateStamp, timezone.utc)
        local_time = utc_time.astimezone()
        print("File compilation time : " + local_time.strftime("%Y-%m-%d %H:%M:%S.%f%z"))
        # import Hash
        print("import HASH : " + str(pe.get_imphash()))
        # SizeOfCode, double world type
        print("SizeOfCode : " + str(pe.OPTIONAL_HEADER.SizeOfCode))
        # MajorLinkerVersion
        print("MajorLinkerVersion : " + str(pe.OPTIONAL_HEADER.MajorLinkerVersion))

        for sec in pe.sections:
            # sec.get_entropy()
            print("section name : " + str(sec.Name)+"\tsection entropy : " + str(sec.get_entropy()))

        print()

    print('total pefile counts = ' + str(len(pefilePathList)))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Wrong")
        print("example) python pefileInfo.py DirPath")
        exit()

    pefilePathList = []
    print("start to parse the file path of PE in directory")
    search(sys.argv[1], pefilePathList)
    print("end")
    print("start to extract the PE info")
    printPEInfo(pefilePathList)