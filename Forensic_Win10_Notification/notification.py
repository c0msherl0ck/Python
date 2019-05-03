import sys
import os
import argparse
import codecs # https://docs.python.org/3.3/library/codecs.html
# euc_kr, iso2022_jp_2, iso2022_kr, johab, cp949

parser = argparse.ArgumentParser(
    usage='notification.py [encoding] [inputFile] [outputFile]',
    description='Extract text from Windows notification center DB',
    epilog='example : notification.py utf-8 wpndatabase.db result.txt'
)
parser.add_argument('encode', type=str, default='utf-8', metavar='encoding option', help='utf-8, cp949, euc-kr.. etc')
parser.add_argument('infile', type=str, metavar='input file', help='wpndatabase.db')
parser.add_argument('outfile', type=str, metavar='output file', help='result.txt')
args = parser.parse_args()

encodingOption = args.encode
inFile = args.infile
outFile = open(args.outfile, 'w')

with open(inFile, 'rb') as f:
    fileSize = os.path.getsize(inFile)
    offset = 0
    XMLOffsetStart = 0
    XMLOffsetEnd = 0
    XMLString = b''
    NextXMLOffsetStart = 0
    textOffsetStart = 0
    textOffsetEnd = 0
    textString = b''

    while 1:
        bytes = f.read(5)
        # end of the file
        if bytes == b'':
            print("this is the end of file")
            break
        # search for <?xml ~ ?>
        if bytes == b'<?xml':
            XMLOffsetStart = offset
            offset = offset + 5
            f.seek(offset)
            while 1:
                bytes = f.read(2)
                if bytes == b'?>':
                    offset = offset + 2
                    XMLOffsetEnd = offset
                    f.seek(XMLOffsetStart)
                    XMLString = f.read(XMLOffsetEnd - XMLOffsetStart)
                    # print()
                    # print(XMLString)
                    # print('XMLOffsetStart = '+str(XMLOffsetStart))
                    # print('XMLOffsetEnd = '+str(XMLOffsetEnd))
                    outFile.write('\n\n')
                    outFile.write(str(XMLString.decode(encodingOption, errors='ignore')))

                    # find next xml start offset
                    while 1:
                        bytes = f.read(5)
                        # end of file
                        if bytes == b'':
                            break
                        if bytes == b'<?xml':
                            NextXMLOffsetStart = offset
                            break
                        else:
                            offset = offset + 1
                            f.seek(offset)
                    # no more xml
                    if NextXMLOffsetStart == XMLOffsetStart:
                        NextXMLOffsetStart = fileSize # end of file

                    # print("NextXMLOffsetStart = " + str(NextXMLOffsetStart))

                    f.seek(XMLOffsetEnd)
                    offset = XMLOffsetEnd
                    # search for <text ... </text> recursively until next xml
                    while offset < NextXMLOffsetStart:
                        bytes = f.read(5)
                        if bytes == b'<text':
                            textOffsetStart = offset
                            offset = offset + 5
                            f.seek(offset)
                            # print('\t' + "textOffsetStart = " + str(textOffsetStart))
                            while offset < NextXMLOffsetStart:
                                bytes = f.read(7)
                                if bytes == b'</text>':
                                    textOffsetEnd = offset + 7
                                    offset = offset + 7
                                    f.seek(textOffsetStart)
                                    textString = f.read(textOffsetEnd - textOffsetStart)
                                    # print('\t' + "textOffsetEnd = " + str(textOffsetEnd))
                                    # print('\t' + "textString = " + str(textString))
                                    print(textString.decode(encodingOption, errors='ignore'))
                                    outFile.write('\n')
                                    outFile.write(str(textString.decode(encodingOption, errors='ignore')))
                                    f.seek(offset)
                                    break
                                else:
                                    offset = offset + 1
                                    f.seek(offset)
                        else:
                            offset = offset + 1
                            f.seek(offset)
                    # end of message block
                    break
                else:
                    offset = offset + 1
                    f.seek(offset)
        else:
            offset = offset + 1
            f.seek(offset)
outFile.close()
print("Finish")


