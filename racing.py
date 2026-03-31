# Turtle Racing game with Betting
from turtle import *
import time
import random
import os

# Set up window
hideturtle()
screen = Screen()
screen.setup(width=500, height=500)
title("Turtle Race")
bgcolor('forestgreen')

turtleColors = ['red', 'blue', 'yellow', 'black', 'purple']
balance = 100
turtles = []
os.system('cls')  # Clear console for better readability

def print_turtles(): # print turtles in order with numbers
    for i, color in enumerate(turtleColors, start=1):
        print(f"{i}. {color}")

# introduction
print("=== TURTLE RACE ===")
print(f"Your starting balance: ${balance}")
print("Available turtles:")
print_turtles()
# Get bet color
while True:
    betColor = textinput("Place Bet", "which turtle do you want to bet on? ").strip().lower()
    if betColor in turtleColors:
        break
    print("Turtle not available. Please choose from the list.")
    print_turtles()

# Get bet amount
while True:
    try:
        betAmount = int(textinput("Bet Amount", "How much do you want to bet? $"))
        if 0 < betAmount <= balance:
            break
        else:
            print("Invalid bet amount. Please enter a valid amount.")
    except:
        print("Invalid input. Please enter a number.")
print()

balance -= betAmount
print(f"You bet ${betAmount} on the {betColor} turtle. Good luck!")
print("Starting race...\n")

# Lane object
lane = Turtle()
lane.hideturtle()
lane.penup()
lane.color('black')
lane.pensize(1)
lane.speed('fastest')
num_lanes = 5
laneHeight = 40
startY = -80

# draw lanes
for i in range(num_lanes + 1):
    y = startY + i * laneHeight - 20
    lane.goto(-220, y)
    lane.pendown()
    lane.goto(220, y)
    lane.penup()

# draw a finish line
finishLine = Turtle()
finishLine.hideturtle()
finishLine.penup()
finishLine.color('black')
finishLine.pensize(5)
finishLine.speed('fastest')
finishLine.goto(220, startY - 20)
finishLine.pendown()
finishLine.goto(220, startY + (num_lanes * laneHeight) - 20)

# display betting info
betDisplay = Turtle()
betDisplay.hideturtle()
betDisplay.penup()
betDisplay.color('white')
betDisplay.goto(0, 200)
betDisplay.write(f"Your bet: ${betAmount} on {betColor} | Balance: ${balance}", align="center", font=("Arial", 16, "normal"))

# instantiate turtles
for paint in turtleColors:
    racer = Turtle(shape='turtle')
    racer.color(paint)
    racer.penup()
    racer.goto(-200, (turtleColors.index(paint) * 40) - 80)
    turtles.append(racer)

# race
winner = None
while not winner:
    for racer in turtles:
        racer.forward(random.randint(1, 10))
        if racer.xcor() >= 200:
            winner = racer.pencolor()
            break

# announce winner
print(f"The winner is the {winner} turtle!")
if betColor == winner:
    winnings = betAmount * 4
    balance += winnings
    resultMessage = f"\nCongratulations! You won ${winnings}.\nYour new balance is ${balance}."
    print(resultMessage)

# result message
else:
    resultMessage = f"\nSorry, you lost your bet.\nYour new balance is ${balance}."
    print(resultMessage)

# Display result on screen
resultDisplay = Turtle()
resultDisplay.hideturtle()
resultDisplay.penup()
resultDisplay.color('white')
resultDisplay.goto(0, -200)
resultDisplay.write(resultMessage, align="center", font=("Arial", 16, "normal"))

# Keep window open
done()