from cs50 import get_string

# put text to check in var
textMain = get_string("Enter text: ")

# var needed for this ex
characterCounter = 0
letterCounter = 0
wordCounter = 1
sentenceCounter = 0

# number of char
characterCounter = len(textMain)

# number of letter
for isLetter in textMain:
    if isLetter.isalpha():
        letterCounter += 1
        
# number of word
for isSpace in textMain:
    if (isSpace == " "):
        wordCounter += 1
        
# number of sentence
for isSentence in textMain:
    if (isSentence == "." or isSentence == "!" or isSentence == "?"):
        sentenceCounter += 1
      
# print(characterCounter)
# print(letterCounter)
# print(wordCounter)
# print(sentenceCounter)

L = letterCounter * 100 / wordCounter
S = sentenceCounter * 100 / wordCounter

# Coleman-Liau index
indexColemanLiau = round(0.0588 * L - 0.296 * S - 15.8)

# check what grade
if (indexColemanLiau < 1):
    print("Before Grade 1")

elif (indexColemanLiau >= 16):
    print("Grade 16+")

else:
    print("Grade ", indexColemanLiau)