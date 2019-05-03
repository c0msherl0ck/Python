def copy_bin_file(filename, targetfile):
    chunk_size = 1024 * 10 ## read by 10KB unit
    cnt = 0
    fileIndex = -1
    with open(filename, 'rb') as f1:
        while True:
            buffer = f1.read(chunk_size)
            # print(buffer)
            bufferStr = buffer.decode('utf-8')
            outputStr = ''
            i = bufferStr.find('2018-') # searching dst_port start pointer
            k = bufferStr.find('2018-') # to remember j, where the space bar is after dst_port
            if not buffer: # if it is end of the data, return
                print('this is the end')
                return
            # per 10MB, increase fileIndex, and make new file
            if cnt % 1000 == 0:
                fileIndex = fileIndex + 1
                print(targetfile + str(fileIndex) + '.txt')
                # create file
                with open(targetfile + str(fileIndex) + '.txt', 'w') as f2:
                    while True:
                        index = bufferStr.find('dst_port', i, len(bufferStr))
                        if index == -1:
                            break
                        # print(bufferStr[len(bufferStr)-1])
                        for j in range(index, len(bufferStr)):
                            if bufferStr[j] == ' ':
                                i = index + 1
                                # print('find spacebar after dst_port :' + str(j) + '$$' + bufferStr[j] + '$$')
                                outputStr = outputStr + bufferStr[k:j] + '\n'
                                # print(outputStr)
                                k = j + 1
                                break
                            else:
                                if j == len(bufferStr)-1:
                                    i = index + 1
                    # print('create : '+outputStr)
                    f2.write(outputStr)
            else:
                # print('append')
                with open(targetfile + str(fileIndex) + '.txt', 'a') as f2:
                    while True:
                        index = bufferStr.find('dst_port', i, len(bufferStr))
                        if index == -1:
                            break
                        # print(bufferStr[len(bufferStr)-1])
                        for j in range(index, len(bufferStr)):
                            if bufferStr[j] == ' ':
                                i = index + 1
                                # print('find spacebar after dst_port :' + str(j) + '$$' + bufferStr[j] + '$$')
                                outputStr = outputStr + bufferStr[k:j] + '\n'
                                # print(outputStr)
                                k = j + 1
                                break
                            else:
                                if j == len(bufferStr)-1:
                                    i = index + 1
                    # print('append : '+outputStr)
                    f2.write(outputStr)
            # count how many times this loop performs
            cnt = cnt + 1
            # print(cnt)

filename = 'F:\\holywater\\firewall\\firewall\\firewall.log'
targetfile = 'F:\\holywater\\firewall\\split\\split_'

copy_bin_file(filename, targetfile)