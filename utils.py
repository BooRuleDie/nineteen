import sqlite3
import datetime

EBCED_DICT = {
    'a': 1, 'b': 2, 'c':3, 'd':4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 
    'j': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 'o': 60, 'p': 70, 'q': 80, 'r': 90, 's': 100, 't': 200, 'u': 300, 'v': 400, 'w': 500, 'x': 600, 'y': 700, 'z': 800
}

def runSQL(SQL, data = (), fetch = False):
    try:
        # writing credentials to the database
        conn = sqlite3.connect('english_words.db')
        cursor = conn.cursor()        
        cursor.execute(SQL, data)
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()

    except sqlite3.Error as e:
        # if there is an error keep it in the errors.log
        now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        with open('errors.log', 'a') as f:
            f.write(now + ': ' + str(e) + '\n\n')

    finally:
        cursor.close()
        conn.close()

def calculatePhase1And2(NUMBER):
    phase1List = []
    for firstNumber in range(1, NUMBER - 2):
        for secondNumber in range(1, NUMBER - firstNumber - 1):
            for thirdNumber in range(1, NUMBER - firstNumber - secondNumber):
                fourthNumber = NUMBER - firstNumber - secondNumber - thirdNumber
                
                numberSet1 = [firstNumber, secondNumber, thirdNumber, fourthNumber]
                numberSet2 = [firstNumber, firstNumber + secondNumber, NUMBER - fourthNumber, NUMBER]
                
                phase1Number = int(f"1{numberSet1[0]}2{numberSet1[1]}3{numberSet1[2]}4{numberSet1[3]}")
                phase2Number = int(f"1{numberSet2[0]}2{numberSet2[1]}3{numberSet2[2]}4{numberSet2[3]}")

                phase1And2 = phase1Number % NUMBER == 0 and phase2Number % NUMBER == 0
                
                if phase1And2:
                    phase1List.append(numberSet1)
    return phase1List

def getWordList(length):
    words = runSQL("SELECT word FROM words WHERE length=?",(length,), fetch=True)
    return [wordList[0] for wordList in words]

def testCaseToEbcedNumbers(testCase):
    resultList = []
    for word in testCase:
        l = []
        for letter in word:
            l.append(EBCED_DICT[letter])
        resultList.append(l)
    return resultList

def calculatePhase3(ebcedNumberList):
    testNumber = f"1{sum(ebcedNumberList[0])}2{sum(ebcedNumberList[1])}3{sum(ebcedNumberList[2])}4{sum(ebcedNumberList[3])}"
    if int(testNumber) % 19 == 0:
        return testNumber
    return False

def calculatePhase4(ebcedNumberList):
    firstPart = sum(ebcedNumberList[0])
    secondPart = sum(ebcedNumberList[1]) + firstPart
    thirdPart = sum(ebcedNumberList[2]) + secondPart
    fourthPart = sum(ebcedNumberList[3]) + thirdPart

    testNumber = f"1{firstPart}2{secondPart}3{thirdPart}4{fourthPart}"
    if int(testNumber) % 19 == 0:
        return testNumber
    return False
    