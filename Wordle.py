import re
import copy
import itertools

WORDLENGTH = 5

def get_input():
    foundLetters = input("Enter letters with known position, zero indexed, separated by a comma (eg: a0,r3) \n >").replace(' ','').split(',')
    inWord = input("Enter letters that are known to be in the word and their possible positions after, zero indexed, separated by commas(eg: a124,r12) \n >").replace(' ','').split(',')
    possible = input("Enter letters that might still be in the word, no spaces (eg: abcd) \n >").replace(' ','') # ex 'abcfiomprq'
    return foundLetters, inWord, possible

def get_words():
    dataset = []
    fileName = 'small_dict.txt'
    with open(fileName, newline = '') as file:
            for line in file:
                dataset.append(line)
    return dataset

def create_pattern(found, inWord, possible):
    foundDictionary = {}
    for i in found:
        foundDictionary[i[1]] = i[0] 
    
    inWordDictionary = {i[0]: i[1:] for i in inWord} # This is DIRTY lambda: int(x) for x in
    allCombinations = list(itertools.product(*inWordDictionary.values()))
    allKeys = list(inWordDictionary.keys())
    allPatterns = []

    for combo in allCombinations:
        if len(set(combo)) < len(combo): # Can't choice same index in output pattern for a letter
            continue
        elif set(foundDictionary.keys()) & set(combo) != set() :
            continue

        currentRE = '^'
        for i in range(WORDLENGTH):
            if str(i) in foundDictionary.keys():
                currentRE += foundDictionary[str(i)]+'{1}' 
                continue

            elif str(i) in combo:
                currentRE += allKeys[combo.index(str(i))]+'{1}'
                continue
            else:
                currentRE += '[' + possible + ']{1}'           
        allPatterns.append(re.compile(currentRE + '$'))
    return allPatterns   

def remove_dups(wordset):
    return list(set(wordset))

def check(words, customRESet):
    found = []
    for word in words:
        word = word.split(chr(10))[0].lower()
        for RE in customRESet:
            if re.match(RE,word):
                found.append(word)
    found = remove_dups(found)

    return found


def main():
    first, second, third = get_input()
    customRE = create_pattern(first,second,third)
    allWords = get_words()
    found = check(allWords,customRE)

    print(f'\n I found these: {sorted(found)}')
    #print(f'\n The custom RE is : {customRE}')

if __name__ == '__main__':
    main()
