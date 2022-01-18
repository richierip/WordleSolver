from ctypes.wintypes import WORD
from os import name
import re
import copy
import itertools
# from itertools import chain, combinations
# def all_subsets(ss):
#     return chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1)))

WORDLENGTH = 5


def get_input():
    foundLetters = input("Enter letters with known position, followed by a comma (eg: a0,r3) \n >").split(',')
    inWord = input("Enter letters that are known to be in the word and their possible positions after, separated by commas(eg: a124,r12) \n >").split(',')
    possible = input("Enter letters that might still be in the word \n >").replace(' ','') # ex 'abcfiomprq'
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
    allPatterns = list(itertools.product(*inWordDictionary.values()))
    allKeys = list(inWordDictionary.keys())

    print(f'\n Here is the custom dict : {inWordDictionary} ')
    print(f'\n Here are all keys : {type(list(inWordDictionary.keys()))} and also {list(inWordDictionary.keys())} ')
    print(f'\n Here are all patterns : {allPatterns} ')
    print(f'\n Here is the fondDict : {foundDictionary} ')

    #allPatterns = all_subsets(inWordDictionary.keys())
    for x in range(0,len(inWord)-1):
        for y in range(x+1, len(inWord)):
            print(f'\n##xy {x} - {y}')
            firstLetter = list(inWordDictionary)[x]
            secondLetter = list(inWordDictionary)[y]
            print(f'##xyletter {firstLetter} - {secondLetter}')

            for firstIndex in inWordDictionary[firstLetter]:
                for secondIndex in inWordDictionary[secondLetter]:
                    print(f'\n##xyindex {firstIndex} - {secondIndex}')
                    if firstIndex == secondIndex:
                        continue
                    cur = '^'
                    for i in range(WORDLENGTH):
                        if str(i) in foundDictionary.keys():
                            cur += foundDictionary[str(i)]+'{1}' 
                            continue

                        elif str(i) == firstIndex:
                            cur += firstLetter+'{1}'
                            continue
                        elif str(i) == secondIndex:
                            cur += secondLetter+'{1}'
                            continue
                        else:
                            cur += '[' + possible + ']{1}'
                            
                    
                    allPatterns.append(cur + '$')

    return allPatterns
            

def remove_dups(wordset):
    return list(set(wordset))


def check(words, customRESet):
    found = []
    test = True
    for word in words:
        word = word.split(chr(10))[0].lower()
        for RE in customRESet:
            if re.match(RE,word):
                found.append(word)
    found = remove_dups(found)

    return found

def main():
    first, second, third = get_input()
    #customRE1 = re.compile('^a{1}(q|w|y|p|f|j|x|v|b){2}e{1}(q|w|y|p|f|j|x|v|b){1}$') # Should use [qwypfjxvb]
    #customRE2 = re.compile('^a{1}e{1}(q|w|y|p|f|j|x|v|b){3}$')
    customRE = create_pattern(first,second,third)

    # allWords = get_words()
    # found = check(allWords,customRE)

    # print(f'\n I found these: {sorted(found)}')

    # print(f'\n The custom RE is : {customRE}')

if __name__ == '__main__':
    main()
