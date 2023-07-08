from utils import calculatePhase1And2
from utils import getWordList, testCaseToEbcedNumbers, calculatePhase3, calculatePhase4

NUMBER = 19

if __name__ == "__main__":
    numberSet = calculatePhase1And2(NUMBER) # [[1, 6, 1, 11], [3, 4, 6, 6], [5, 1, 2, 11]]
    
    for set in numberSet:
        firstWordList = getWordList(set[0])
        secondWordList = getWordList(set[1])
        thirdWordList = getWordList(set[2])
        fourthWordList = getWordList(set[3])
        

        for firstWordListItem in firstWordList:
            for secondWordListItem in secondWordList:
                for thirdWordListItem in thirdWordList:
                    for fourthWordListItem in fourthWordList:
                        testCase = [
                            firstWordListItem,
                            secondWordListItem,
                            thirdWordListItem,
                            fourthWordListItem
                            ]
                        
                        ebcedNumberList = testCaseToEbcedNumbers(testCase)
                        phase3Number = calculatePhase3(ebcedNumberList)
                        phase4Number = calculatePhase4(ebcedNumberList)
                        if phase3Number and phase4Number:
                            print(testCase)
                            print(ebcedNumberList)
                            print(phase3Number)
                            print(phase4Number)
                        
                        

