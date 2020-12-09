from cs50 import get_int

numberOfLines = get_int("How many lines?: ")
blankSpace = " "
hashBlock = "#"

if numberOfLines < 1 or numberOfLines > 8:
    print("Error, must be superior to 0 and less than 8")
    numberOfLines = get_int("How many lines?: ")
    
for counter in range(numberOfLines):
    print((blankSpace * (numberOfLines - counter - 1)) + (hashBlock * (counter + 1)))
    