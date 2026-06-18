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
        print(f" #{self.raceNumber} — {self.name} the {self.species}\n")
        print(f"{equal40}\n")
        print(f" Color: {self.color}\n")
        print(f" Age: {self.age} years old\n")
        print(f" Weight: {self.weight} kg\n")
        print(f" Height: {self.height} cm\n")
        print(f"\n {self.bio}\n")
        print(f"{equal40}")

# Bio s
tracyFile = open("tracy.txt")
ralphFile = open("ralph.txt")
jennyFile = open("jenny.txt")
dougFile = open("doug.txt")
pamFile = open("pam.txt")

tracyBio = print(tracyFile.read())
ralphBio = print(ralphFile.read())
jennyBio = print(jennyFile.read())
dougBio = print(dougFile.read())
pamBio = print(pamFile.read())

# Create turtle racer instances
Tracy = Racers("Tracy", "black", 124, "Sea Turtle", 150, 120, 50, tracyBio)
Ralph = Racers("Ralph", "red", 267, "Land Turtle", 100, 80, 30, ralphBio)
Jenny = Racers("Jenny", "yellow", 376, "Box Turtle", 50, 30, 20, jennyBio)
Doug = Racers("Doug", "blue", 408, "Leatherback Turtle", 200, 150, 70, dougBio)
Pam = Racers("Pam", "purple", 512, "Green Sea Turtle", 120, 100, 40, pamBio)

turtleRacers = [Tracy, Ralph, Jenny, Doug, Pam]

# Setup screen once
screen = Screen()
screen.setup(width=500, height=500)

balance = 100

def show_turtles():
    for turtle in turtleRacers:
        print(f"{turtle.name.title()}: {turtle.color}")

def clear_everything():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def show_title():
    print("=== TURTLE RACE ===")
    print(f"Your current balance: {balance} shells")
    print("Available turtles:")
    show_turtles()

# -----MAIN GAME LOOP-----
while balance > 0:
    hideturtle()
    screen.bgcolor('forestgreen')
    title("Turtle Race")
    
    clear_everything()
    
    # 1. View Turtle Info Loop
    while True:
        show_title()
        turtleChoice = textinput("Turtle Info", "Enter the name of a turtle you want to learn about (or '0' to skip): ")
        if turtleChoice is None or turtleChoice.strip() == '0':
            clear_everything()
            break
        
        turtleChoice = turtleChoice.strip().lower()
        if turtleChoice in [t.name.lower() for t in turtleRacers]:
            for turtle in turtleRacers:
                if turtle.name.lower() == turtleChoice:
                    turtle.displayInfo()
                    input("\nPress Enter to continue...")  # Pauses to let user read console
                    clear_everything()
                    break
        else:
            clear_everything()
            print("Invalid choice. Please enter a name from the list.\n")

    # 2. Bet Selection Loop
    while True:
        show_title()
        betName = textinput("Place Bet", "Which turtle do you want to bet on? ")
        if betName is None:
            continue
        betName = betName.strip().lower()
        if betName in [t.name.lower() for t in turtleRacers]:
            betName = betName.title()
            clear_everything()
            break
        else:
            clear_everything()
            print("Invalid choice. Please enter a name from the list.\n")

    # 3. Bet Amount Loop
    while True:
        show_title()
        try:
            betAmount = textinput("Bet Amount", f"How much do you want to bet? (1-{balance} shells)")
            if betAmount is None:
                continue
            betAmount = int(betAmount)
            if 0 < betAmount <= balance:
                break
            else:
                clear_everything()
                print(f"Invalid bet amount. Enter a number between 1 and {balance}.\n")
        except ValueError:
            clear_everything()
            print("Invalid input. Please enter a whole number.\n")

    clear_everything()
    balance -= betAmount
    print(f"You bet {betAmount} shells on the {betName} turtle. Good luck!")
    print("Starting race...\n")

    # Draw Lanes
    lane = Turtle()
    lane.hideturtle()
    lane.penup()
    lane.color('black')
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

    # Draw Finish Line
    finishLine = Turtle()
    finishLine.hideturtle()
    finishLine.penup()
    finishLine.color('black')
    finishLine.pensize(5)
    finishLine.speed('fastest')
    finishLine.goto(220, startY - 20)
    finishLine.pendown()
    finishLine.goto(220, startY + (num_lanes * laneHeight) - 20)

    # Draw Top Text
    betDisplay = Turtle()
    betDisplay.hideturtle()
    betDisplay.penup()
    betDisplay.color('white')
    betDisplay.goto(0, 200)
    betDisplay.write(f"Your bet: {betAmount} shells on {betName} | Balance: {balance} shells", align="center", font=("Arial", 16, "normal"))

    # Spawn Turtle Racers
    racer_objects = []
    for turtle in turtleRacers:
        racer = Turtle(shape='turtle')
        racer.color(turtle.color)
        racer.penup()
        racer.goto(-200, (turtleRacers.index(turtle) * 40) - 80)
        racer_objects.append(racer)

    # Core Racing Engine Loop
    winner = None
    while not winner:
        for racer in racer_objects:
            racer.forward(random.randint(1, 10))
            if racer.xcor() >= 200:
                winner_index = racer_objects.index(racer)
                winner = turtleRacers[winner_index].name
                break

    print(f"The winner is the {winner} turtle!")

    # Calculate Payouts
    if betName == winner:
        winnings = betAmount * 4
        balance += winnings
        resultMessage = f"Congratulations! You won {winnings} shells.\nYour new balance is {balance} shells."
    else:
        resultMessage = f"Sorry, you lost your bet.\nYour new balance is {balance} shells."

    print(resultMessage)

    # Display Winner Text on Window
    resultDisplay = Turtle()
    resultDisplay.hideturtle()
    resultDisplay.penup()
    resultDisplay.color('white')
    resultDisplay.goto(0, -200)
    resultDisplay.write(resultMessage, align="center", font=("Arial", 14, "normal"))

    # Pause to let the user see the screen, then wipe it clean for the next round
    time.sleep(4)
    screen.clearscreen()

# Game Over Out of Money Sequence
clear_everything()
print("=== GAME OVER ===")
print("You have run out of shells! Thanks for playing.")
time.sleep(3)
sys.exit()
