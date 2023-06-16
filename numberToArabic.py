EBCED_DICT = {
    1: 'ا', 2: 'ب', 3: 'ج', 4: 'د', 5: 'ه', 6: 'و', 7: 'ز', 8: 'ح', 9: 'ط',
    10: 'ي', 20: 'ك', 30: 'ل', 40: 'م', 50: 'ن', 60: 'س', 70: 'ع', 80: 'ف', 90: 'ص',
    100: 'ق', 200: 'ر', 300: 'ش', 400: 'ت', 500: 'ث', 600: 'خ', 700: 'ذ', 800: 'ض', 900: 'ظ',
    1000: 'غ'
}

with open('phase5.txt', 'r', encoding="utf-8") as file:
    # Read in each line of the file and remove any trailing whitespace
    lines = [line.strip() for line in file.readlines()]

for line in lines:
    sections = line.split('-')
    sentence = ''
    for section in sections:
        # Strip off the enclosing square brackets and split the remaining string by commas
        nums = section[1:-1].split(',')
        for num in nums:
            sentence += EBCED_DICT[int(num)]
        # add space at the end of every word
        sentence += " "
    
    with open("arabic.txt", "a", encoding="utf-8") as fp:
        fp.write(sentence + "\n")
    
