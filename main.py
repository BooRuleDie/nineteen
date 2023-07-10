from utils import getWordList, calculatePhase1And2, testCaseToEbcedNumbers, calculatePhase3, calculatePhase4, calculatePhase5, calculatePhase6, printProgress, cumilativeSum, writeResult
import time

NUMBER = 19

if __name__ == "__main__":
    numberSet = calculatePhase1And2(NUMBER) # [[1, 6, 1, 11], [3, 4, 6, 6], [5, 1, 2, 11]]
    start = time.time()
    
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
                        
                        set2 = cumilativeSum(set)
                        phase1Number = f"1{set[0]}2{set[1]}3{set[2]}4{set[3]}"
                        phase2Number = f"1{set2[0]}2{set2[1]}3{set2[2]}4{set2[3]}"
                        phase3Number = calculatePhase3(ebcedNumberList)
                        phase4Number = calculatePhase4(ebcedNumberList)
                        phase5Number = calculatePhase5(ebcedNumberList)
                        phase6Number = calculatePhase6(ebcedNumberList)
                        
                        if phase3Number and phase4Number and phase5Number and phase6Number:
                            writeResult(testCase, phase1Number, phase2Number, phase3Number, phase4Number, phase5Number, phase6Number)
                            printProgress(testCase[0], start)
                        
                        