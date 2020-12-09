from cs50 import get_float


# varibales
priceInDollar = 0
princeInCents = 0
quarter = 0
dime = 0
nickel = 0
penny = 0

# ask for the price in dollar
priceInDollar = get_float("$")

#  check if input is correct
if (priceInDollar < 0):
    priceInDollar = get_float("$")
    
# convert to cent
princeInCents = round(priceInDollar * 100, 0)

# start the counting   
while (princeInCents > 0):
    
    # quarter
    if (princeInCents >= 25):
        princeInCents -= 25
        quarter += 1
    
    #  dime    
    elif (princeInCents >= 10):
        princeInCents -= 10
        dime += 1
    
    # nickel    
    elif (princeInCents >= 5):
        princeInCents -= 5
        nickel += 1
    # penny    
    else:
        princeInCents -= 1
        penny += 1

# print the total coin owned        
print(quarter + dime + nickel + penny)