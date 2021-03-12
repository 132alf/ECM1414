import bitstring
from bitstring import BitArray
import heapq
name = input("please enter file name  \n")
data = str(open(name,"r").readlines())
def findCharacterInstances(data):
    characterInstances = dict()
    for character in data:
        characterInstances[character]=characterInstances.get(character,0)+1
    return characterInstances
def constructTree(frequency):
    tree = [[weight, [character, '']] for character, weight in frequency.items()]
    heapq.heapify(tree)
    while len(tree) > 1:
        low = heapq.heappop(tree)
        high = heapq.heappop(tree)
        for item in low[1:]:
            item[1] = '0' + item[1]
        for item in high[1:]:
            item[1] = '1' +item[1]
        heapq.heappush(tree, [low[0] + high[0]] + low[1:] + high[1:])
    return sorted(heapq.heappop(tree)[1:])
def huffmanEncode(data):
    characterCodes = dict()
    tree = constructTree(findCharacterInstances(data))
    for i in tree:
        characterCodes[i[0]] = i[1]
    bitOutput = BitArray()
    for character in data:
        bitOutput.append('0b'+characterCodes[character])
    compressedFile = open("compressed" + name,"wb+")
    compressedFile.write(bitOutput.tobytes())
huffmanEncode(data)
def huffmanDecode(encodedText):
    characterCodes = dict()
    tree = constructTree(findCharacterInstances(data))
    for i in tree:
        characterCodes[i[0]] = i[1]
    outputString = ""
    codeString = ""
    for bit in BitArray(encodedText).bin:
        codeString += str(bit)
        for character in characterCodes:
            if characterCodes[character] == codeString:
                outputString += character
                codeString = ""
    uncompressedFile = open("uncompressed" + name,"w+")
    outputString = outputString[:-5]
    outputString = outputString[2:]
    uncompressedFile.write(outputString)
huffmanDecode(open("compressed"+name,"rb").read())