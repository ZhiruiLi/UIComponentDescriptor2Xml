import AS2MXMLParser
if __name__ == '__main__':
    (readWriteDict, tagPrefixDict, defPrefix) = AS2MXMLParser.configParser()
    for (k, v) in readWriteDict.items():
        AS2MXMLParser.fromFileToFile(k, tagPrefixDict, defPrefix, v)