import datetime
import itertools
import asyncio
import aiofiles
import aiohttp

NUMBER = 19

EBCED = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 
    10, 20, 30, 40, 50, 60, 70, 80, 90,
    100, 200, 300, 400, 500, 600, 700, 800, 900, 
    1000
]
    
async def cumulativeSum(List):
    cumulativeList = []
    cumulativeSum = 0

    for num in List:
        cumulativeSum += num
        cumulativeList.append(cumulativeSum)
    return cumulativeList

async def createNumberPhase5Or6(Phase5Or6List):    
    resultString = ""

    for item in Phase5Or6List:
        if isinstance(item, str):
            resultString += item
        elif isinstance(item, list):
            subResultString = "".join([str(sub_item) for sub_item in item])
            resultString += subResultString          
    return int(resultString)

async def writeFile(filename, text):
    async with aiofiles.open(filename, 'a') as f:
        await f.write(text)

async def sendTelegramMessage(TOKEN, chat_id, message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
        except aiohttp.ClientError:
            now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            await writeFile("errors.log", f"{now} : Failed while sending Telegram Message!")

async def calculatePhase1And2():
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

async def calculatePhase3To6(phase1List):
    # process bar variables
    total_permutations = len(phase1List) * (len(EBCED) ** NUMBER)
    processed_permutations = 0
    percentage_progress = 0
    
    for phaseList in phase1List:
        for permutation in itertools.product(EBCED, repeat=NUMBER):
            
            # send the process bar through a telegram bot if it's increased by one
            processed_permutations += 1
            if percentage_progress < int((processed_permutations / total_permutations) * 100):
                percentage_progress = int((processed_permutations / total_permutations) * 100)
                await sendTelegramMessage("5604425500:AAEC06kO1U_WrhMD38ZbxLSAB3pEIGh1KiI", "5130853265", f"Progress: {percentage_progress}%")
            
            permutation = list(permutation)
            phase3List = [
                "1", sum(permutation[0:phaseList[0]]), 
                "2", sum(permutation[phaseList[0]:sum(phaseList[:2])]), 
                "3", sum(permutation[sum(phaseList[:2]):sum(phaseList[:3])]), 
                "4", sum(permutation[sum(phaseList[:3]):])
                ]
        
            phase4List = [
                "1", phase3List[1], 
                "2", phase3List[1] + phase3List[3], 
                "3", phase3List[1] + phase3List[3] + phase3List[5], 
                "4", phase3List[1] + phase3List[3] + phase3List[5] + phase3List[7]
                ]
            
            phase5List = [
                "1", permutation[0:phaseList[0]],
                "2", permutation[phaseList[0]:sum(phaseList[:2])],
                "3", permutation[sum(phaseList[:2]):sum(phaseList[:3])],
                "4", permutation[sum(phaseList[:3]):]
            ]

            cumulativeSumList = await cumulativeSum(permutation)
            phase6List = [
                "1", cumulativeSumList[0:phaseList[0]],
                "2", cumulativeSumList[phaseList[0]:sum(phaseList[:2])],
                "3", cumulativeSumList[sum(phaseList[:2]):sum(phaseList[:3])],
                "4", cumulativeSumList[sum(phaseList[:3]):]
            ]

            phase3Number = int("".join(map(str, phase3List)))
            phase4Number = int("".join(map(str, phase4List)))
            phase5Number = await createNumberPhase5Or6(phase5List)
            phase6Number = await createNumberPhase5Or6(phase6List)

            condition = phase3Number % NUMBER == 0 and phase4Number % NUMBER == 0 and phase5Number % NUMBER == 0 and phase6Number % NUMBER == 0 
            
            if condition:
                phase1Number = int(f"1{phaseList[0]}2{phaseList[1]}3{phaseList[2]}4{phaseList[3]}")
                phase2List = await cumulativeSum(phaseList)
                phase2Number = int(f"1{phase2List[0]}2{phase2List[1]}3{phase2List[2]}4{phase2List[3]}")

                result1 = phase1Number / NUMBER
                result2 = phase2Number / NUMBER
                result3 = phase3Number / NUMBER
                result4 = phase4Number / NUMBER
                result5 = phase5Number / NUMBER
                result6 = phase6Number / NUMBER

                formattedString = f"""\
Phase1: {phaseList} -> {phase1Number} = {NUMBER} x {result1:,}
Phase2: {phase2List} -> {phase2Number} = {NUMBER} x {result2:,}
Phase3: {phase3List} -> {phase3Number} = {NUMBER} x {result3:,}
Phase4: {phase4List} -> {phase4Number} = {NUMBER} x {result4:,}
Phase5: {phase5List} -> {phase5Number} = {NUMBER} x {result5:,}
Phase6: {phase6List} -> {phase6Number} = {NUMBER} x {result6:,}


"""             
                phase5TextFormat = f"""\
{phase5List[1]}-{phase5List[3]}-{phase5List[5]}-{phase5List[7]}
"""
                await writeFile("nineteen.txt", formattedString)
                await writeFile("phase5.txt", phase5TextFormat)
                

async def main():
    phase1List = await calculatePhase1And2()
    await calculatePhase3To6(phase1List)

if __name__ == "__main__":
    asyncio.run(main())