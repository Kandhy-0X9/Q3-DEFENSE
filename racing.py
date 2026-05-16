from turtle import *
import time
import random
import os
import sys  

equal40 = "=" * 40
# Define the Racers class to store information about each turtle racer
class Racers:
    def __init__(self, name, color, raceNumber, species, weight, height, age, bio):
        self.name = name
        self.color = color
        self.raceNumber = raceNumber
        self.species = species
        self.weight = weight
        self.height = height
        self.age = age
        self.bio = bio

    def displayInfo(self):
        print(f"\n{equal40}\n")
        print(f"  #{self.raceNumber} — {self.name} the {self.species}\n")
        print(f"{equal40}\n")
        print(f"  Color:   {self.color}\n")
        print(f"  Age:     {self.age} years old\n")
        print(f"  Weight:  {self.weight} kg\n")
        print(f"  Height:  {self.height} cm\n")
        print(f"\n  {self.bio}\n")
        print(f"{equal40}")

# Load turtle bios from text files
tracyBio = file = open("tracy.txt", "r").read()
ralphBio = file = open("ralph.txt", "r").read()
jennyBio = file = open("jenny.txt", "r").read()
dougBio = file = open("doug.txt", "r").read()
pamBio = file = open("pam.txt", "r").read()

# Create turtle racer instances
Tracy = Racers("Tracy", "black", 124, "Sea Turtle", 150, 120, 50, tracyBio)
Ralph = Racers("Ralph", "red", 267, "Land Turtle", 100, 80, 30, ralphBio)
Jenny = Racers("Jenny", "yellow", 376, "Box Turtle", 50, 30, 20, jennyBio)
Doug = Racers("Doug", "blue", 408, "Leatherback Turtle", 200, 150, 70, dougBio)
Pam = Racers("Pam", "purple", 512, "Green Sea Turtle", 120, 100, 40, pamBio)

turtleRacers = [Tracy, Ralph, Jenny, Doug, Pam]

hideturtle()
screen = Screen()
screen.setup(width=500, height=500)
title("Turtle Race")
bgcolor('forestgreen')
balance = 100

# Function to display available turtles and their colors
def show_turtles():
    for turtle in turtleRacers:
        print(f"{turtle.name.title()}: {turtle.color}")
def clear_everything():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')  

# Function to display the title and starting balance
def show_title():
    print("=== TURTLE RACE ===")
    print(f"Your starting balance: {balance} shells")
    print("Available turtles:")
    show_turtles()

# -----MAIN PROGRAM STARTS HERE-----

clear_everything()
# Main loop to allow users to view turtle information before placing a bet
while True:
    show_title()
    turtleChoice = textinput("Turtle Info", "Enter the name of a turtle you want to learn about (or '0' to skip): ")
    if turtleChoice is None:
        break
    turtleChoice = turtleChoice.strip().lower()
    if turtleChoice == '0':
        break
    elif turtleChoice in [turtle.name.lower() for turtle in turtleRacers]:
        for turtle in turtleRacers:
            if turtle.name.lower() == turtleChoice:
                turtle.displayInfo()
                clear_everything()
                break
    else:
        print("Invalid choice. Please enter a name from the list or '0' to skip.")

while True:
    show_title()
    betName = textinput("Place Bet", "which turtle do you want to bet on? ").strip().lower()
    if betName in [turtle.name.lower() for turtle in turtleRacers]:
        betName = betName.title()
        break
    else:
        print("Invalid choice. Please enter a name from the list.")

while True:
    try:
        betAmount = int(textinput("Bet Amount", "How much do you want to bet? shells"))
        if 0 < betAmount <= balance:
            break
        else:
            print("Invalid bet amount. Please enter a valid amount.")
    except:
        print("Invalid input. Please enter a number.")
print()

balance -= betAmount
print(f"You bet {betAmount} shells on the {betName} turtle. Good luck!")
print("Starting race...\n")

lane = Turtle()
lane.hideturtle()
lane.penup()
lane.color('black')
lane.pensize(1)
lane.speed('fastest')
num_lanes = 5
laneHeight = 40
startY = -80

for i in range(num_lanes + 1):
    y = startY + i * laneHeight - 20
    lane.goto(-220, y)
    lane.pendown()
    lane.goto(220, y)
    lane.penup()

finishLine = Turtle()
finishLine.hideturtle()
finishLine.penup()
finishLine.color('black')
finishLine.pensize(5)
finishLine.speed('fastest')
finishLine.goto(220, startY - 20)
finishLine.pendown()
finishLine.goto(220, startY + (num_lanes * laneHeight) - 20)

betDisplay = Turtle()
betDisplay.hideturtle()
betDisplay.penup()
betDisplay.color('white')
betDisplay.goto(0, 200)
betDisplay.write(f"Your bet: {betAmount} shells on {betName} | Balance: {balance} shells", align="center", font=("Arial", 16, "normal"))

# Create turtle graphics racers
racer_objects = []
for turtle in turtleRacers:
    racer = Turtle(shape='turtle')
    racer.color(turtle.color)
    racer.penup()
    racer.goto(-200, (turtleRacers.index(turtle) * 40) - 80)
    racer_objects.append(racer)

winner = None
while not winner:
    for racer in racer_objects:
        racer.forward(random.randint(1, 10))
        if racer.xcor() >= 200:
            winner_index = racer_objects.index(racer)
            winner = turtleRacers[winner_index].name
            break

print(f"The winner is the {winner} turtle!")
if betName == winner:
    winnings = betAmount * 4
    balance += winnings
    resultMessage = f"\nCongratulations! You won {winnings} shells.\nYour new balance is {balance} shells."
    print(resultMessage)

else:
    resultMessage = f"\nSorry, you lost your bet.\nYour new balance is {balance} shells."
    print(resultMessage)
    if balance == 0:
        time.sleep(5)
        clear_everything()
        sys.exit()

resultDisplay = Turtle()
resultDisplay.hideturtle()
resultDisplay.penup()
resultDisplay.color('white')
resultDisplay.goto(0, -200)
resultDisplay.write(resultMessage, align="center", font=("Arial", 16, "normal"))

done()