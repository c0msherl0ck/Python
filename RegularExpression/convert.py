import sys
import re

if __name__ == "__main__":
    f = open(sys.argv[1],'r')
    f2 = open("rime.html",'w')
    f2.write("<!DOCTYPE html>"+"\n"
             +"<html xmlns=\"http://www.w3.org/1999/xhtml\">"+"\n"
             +"<head>"+"\n"
             +"<title>THE RIME OF THE ANCYENT MARINERE, IN SEVEN PARTS.</title>"+"\n"
             +"<meta charset=\"utf-8\"/>"+"\n"
             +"</head>"+"\n"
             +"<body>"+"\n")
    # set the Regex object
    regex_h1 = re.compile("(^T.*$)")
    regex_h2 = re.compile("(^[A-Z]*\.$)")
    regex_p1 = re.compile("(^H.*$)")
    regex_p2_start = re.compile("(It.*$)") # 하나 나오면 더 이상 안찾도록 예외처리
    regex_p2_end = re.compile("(H.*morn\.$)")
    # p2 태그가 시작부터 끝까지 line 의 마지막에 br 태그 추가
    # 예외사항1 h2 태그에 속하는 문자열
    # 예외사항2 'Twas ~ ight
    regex_notbr = re.compile("('Twas.*ight.*$)")

    isP2 = 0 # 두번째 P 태그 내부의 문자열인지 확인
    isP2First = 0 # 두번재 P 태그의 시작이 한번 나오면 그 다음부터 정규식 체크를 안하도록 하기 위함

    while True:
        line = f.readline()
        # rime.txt 의 마지막
        if not line:
            f2.write("</body>\n</html>")
            break
        # h1
        if regex_h1.search(line) != None:
            result = re.sub("(^T.*$)", "<h1>"+r'\1'+"</h1>", line)
            f2.write(result)
            f2.write(line) # h1 태그 및에 원래 문자열이 한번 더 나온다.
            continue
        # h2
        if regex_h2.search(line) != None:
            result = re.sub("(^[A-Z]*)", "<h2>" + r'\1' + "</h2>", line) # subtract "."
            result = result.replace(".","")
            f2.write(result)
            continue
        # p1
        if regex_p1.search(line) != None:
            result = re.sub("(^H.*$)", "<p>" + r'\1' + "</p>", line)
            f2.write(result)
            continue
        # p2
        if isP2First == 0:
            if regex_p2_start.search(line) != None:
                isP2 = 1
                isP2First = 1
                result = re.sub("(It.*$)", "<p>" + r'\1' + "</br>", line)
                f2.write(result)
                continue
        if regex_p2_end.search(line) != None:
            isP2 = 0
            result = re.sub("(H.*morn\.$)", r'\1' + "</p>", line)
            f2.write(result)
            continue
        # br 태그
        if isP2 == 1:
            if regex_notbr.search(line) != None: # notbr 에 해당하는 경우
                f2.write(line)
                continue
            else: # notbr 에 해당하는 경우가 아닐 경우
                if line != "\n":
                    result = re.sub("(.+$)", r'\1' + "<br/>", line)
                    f2.write(result)
                    continue
                else: # 두번째 p 태그 내의 개행문자
                    f2.write("<br/>\n")
                    continue
        # 위의 어떤 경우에도 속하지 않는 경우 있는 그대로 write
        f2.write(line)

    f.close()
    f2.close()

