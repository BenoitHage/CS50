textMain = "Test test!"
letterCounter = 0

for isLetter in textMain:
    if isLetter.isalpha():
        letterCounter += 1
        print(letterCounter)
        
        
# number of letter
for isLetter in textMain:
    testCurrent = isLetter.isAlpha()
    if (testCurrent == True):
        letterCounter += 1