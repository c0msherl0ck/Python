import pymysql

conn = pymysql.connect(host='localhost', user='root', password='root',
                       db='firewall', charset='utf8')
curs = conn.cursor()
# sql = "insert into firewalldb(time,src_mac,dst_mac,src_ip,dst_ip,length,srcport,dst_port)values(1,2,3,4,5,6,7,8);"
# sql = "select * from firewalldb"
# rows = curs.fetchall()
# print(rows)
# rows = curs.fetchall()
# print(rows)
# conn.commit()
# conn.close()

def parsingToInt(buffer):
    elements = buffer.split()
    result = []
    time = elements[0] + elements[1]
    time = time.replace('-', '')
    time = time.replace(':', '')
    time = int(time)

    src_mac = elements[11]
    src_mac = src_mac.replace('src_mac=', '')
    src_mac = src_mac.replace(':', '')
    src_mac = src_mac.replace('.', '')
    src_mac = src_mac.replace(',', '')
    src_mac = int(src_mac, 16)

    dst_mac = elements[12]
    dst_mac = dst_mac.replace('dst_mac=', '')
    dst_mac = dst_mac.replace(':', '')
    dst_mac = dst_mac.replace('.', '')
    dst_mac = dst_mac.replace(',', '')
    dst_mac = int(dst_mac, 16)

    src_ip = elements[13]
    src_ip = src_ip.replace('src_ip=', '')
    src_ip = src_ip.replace('.', '')
    src_ip = int(src_ip)

    dst_ip = elements[14]
    dst_ip = dst_ip.replace('dst_ip=', '')
    dst_ip = dst_ip.replace('.', '')
    dst_ip = int(dst_ip)

    length = elements[15]
    length = length.replace('length=', '')
    length = int(length)

    srcport = elements[16]
    srcport = srcport.replace('srcport=', '')
    srcport = int(srcport)

    dst_port = elements[17]
    dst_port = dst_port.replace('dst_port=', '')
    dst_port = int(dst_port)

    result.append(time)
    result.append(src_mac)
    result.append(dst_mac)
    result.append(src_ip)
    result.append(dst_ip)
    result.append(length)
    result.append(srcport)
    result.append(dst_port)

    # print('time ' + str(time))
    # print('src_mac ' + str(src_mac))
    # print('dst_mac ' + str(dst_mac))
    # print('src_ip ' + str(src_ip))
    # print('dst_ip ' + str(dst_ip))
    # print('length ' + str(length))
    # print('srcport ' + str(srcport))
    # print('dst_port ' + str(dst_port))

    return result

srcPath = 'F:\\holywater\\firewall\\split\\split_'
errorPath = 'F:\\holywater\\firewall\\error\\error.txt'
startOfFiles = 0 # split_x.txt 에서의 x 인자
endOfFiles = 3000 # split_y.txt 에서의 y 인자
# 이를 통해 split_number.txt 를 선택하여 DB 에 저장할 수 있다.
numberOfError = 0
numberOfData = 0

f2 = open(errorPath, 'a')
for j in range(startOfFiles,endOfFiles): # select .txt files to push DB
    srcFile = srcPath + str(j) + '.txt'
    print('pushing' + srcFile + 'starts')
    f = open(srcFile, 'r')
    buffers = f.readlines()
    for i in range(0,len(buffers)):
        try:
            elements = parsingToInt(buffers[i])
        except ValueError:
            # write error to 'error.txt'
            # print('Error : '+buffers[i]) # error data
            f2.write(buffers[i])
            numberOfError = numberOfError + 1
            numberOfData = numberOfData + 1
        else:
            # push to DB
            sql = """insert into firewalldb(time,src_mac,dst_mac,src_ip,dst_ip,length,srcport,dst_port)
            values(%s,%s,%s,%s,%s,%s,%s,%s);"""
            curs.execute(sql,(elements[0],elements[1],elements[2],elements[3],elements[4],elements[5],elements[6],elements[7]))
            # print(elements)
            numberOfData = numberOfData + 1
    f.close()
    print('pushing'+srcFile+' ends')
f2.close()

print(numberOfError)
print(numberOfData)

conn.commit()
conn.close()