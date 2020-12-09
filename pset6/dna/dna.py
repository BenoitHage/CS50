import sys

nucleotideBase = []
scoresArray = []
peopleArray = []
occurencesArray = []


# Check if the number of argv is 3

if len(sys.argv) != 3:
    print("python dna.py databases/small.csv sequences/(number).txt")

# Create an array with all the nucleotide bases

with open(sys.argv[1]) as nucleotideDatabase:
    nucleotideBase = nucleotideDatabase.readlines()[0]
    nucleotideBase = nucleotideBase.rstrip()
    nucleotideBase = nucleotideBase.split(",")
    nucleotideBase.pop(0)
    # print(nucleotideBase)

# Create an array with all the names

with open(sys.argv[1]) as peopleDatabase:
    peopleArray = peopleDatabase.readlines()
    peopleCounter = 0
    for peopleElement in peopleArray:
        peopleArray[peopleCounter] = peopleArray[peopleCounter].rstrip()
        peopleArray[peopleCounter] = peopleArray[peopleCounter].split(",")
        peopleArray[peopleCounter] = peopleArray[peopleCounter].pop(0)
        peopleCounter += 1
    peopleArray.pop(0)
    # print(peopleArray)

# Create an array with all the occurences of consecutive nucleotides runs

with open(sys.argv[1]) as scoresDatabase:
    occurencesArray = scoresDatabase.readlines()
    occurencesCounter = 0
    for scoresElement in occurencesArray:
        occurencesArray[occurencesCounter] = occurencesArray[occurencesCounter].rstrip()
        occurencesArray[occurencesCounter] = occurencesArray[occurencesCounter].split(",")
        occurencesArray[occurencesCounter].pop(0)
        occurencesCounter += 1
    occurencesArray.pop(0)
    # print(occurencesArray)

# Read file with DNA sequence

with open(sys.argv[2]) as sequences:
    dnaSequence = sequences.read()
    # print(dnaSequence)

# function to loop through the given DNA and check for consecutive runs


def dnaLooper(nucleotide):
    tempArray = []
    for repetition in range(len(dnaSequence)):
        if nucleotide * repetition in dnaSequence:
            tempArray.append(repetition)
    return tempArray[-1]

# Function to loop through nucleotides and check with dnaLooper for consecutive runs then append to scoresArray


def nucleotideLooper():
    counterNucleotide = 0
    for elementNucleotide in nucleotideBase:
        scoresArray.append(str(dnaLooper(elementNucleotide)))

# Loop through occurencesArray to check for match in scoresArray then print it


nucleotideLooper()
matchCounter = 0
matchPerson = "No match"
for matchElement in occurencesArray:
    if occurencesArray[matchCounter] == scoresArray:
        matchPerson = peopleArray[matchCounter]
    matchCounter += 1
    
print(matchPerson)