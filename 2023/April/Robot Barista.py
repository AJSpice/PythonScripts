#robot barista

#establish menu
menu = "Black Coffee, Espresso, Latte, Cappucino, Frappuccino"

#ask the customer their name
print ("Hello! Welcome to Spicey Coffee.")
customername = input ("What is your name? \n\n")

#checks to see if the customer is on the blacklist
if customername.lower() == "ben" or customername.lower() == "patricia" or customername.lower() == "loki":
    #checks their moral compass and good deeds to see if they can get in
    moralcompass= input ("\nAre you evil?\n")
    if moralcompass.lower() in ["yes", "y"]:
        good_deeds = int (input ("\nHow many good deeds have you done today?\n"))
        if good_deeds < 4:
            deficit = 4 - good_deeds
            print ("\nGet outa here!\nYou need to do " + str(deficit) + " more good deed(s) to be let in")
            exit()
        else:
            print("\nAlright you can order, but you're on thin ice buddy...")
else:
    print ("\nWelcome in " + customername + "!")

#set the price of the coffee
while True:
    order = input ("\nWhat would you like today? Our menu is the following \n\n" + menu + "\nYou can only select one item at a time\n")
    if   order.lower() == "frappuccino":
        price = 13
        break
    elif order.lower() == "black coffee":
        price = 2
        break
    elif order.lower() == "espresso":
        price = 3
        break
    elif order.lower() == "latte":
        price = 4
        break
    elif order.lower() == "cappucino":
        price = 6
        break
    else:
        print("Sorry we don't have that here. Please try again")
        price = 0

#ask the customer how many items they want
quantity = input ("\nOkay, so your order is for a " + order.lower() + "? How many would you like?\n")

#quikmafs
total = int(quantity) * price
print ("\nOkay! Your total is going to be: $" + str(total)+ "\n")
