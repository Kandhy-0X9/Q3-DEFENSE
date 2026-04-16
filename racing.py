from turtle import *
import time
import random
import os
import sys

hideturtle()
screen = Screen()
screen.setup(width=500, height=500)
title("Turtle Race")
bgcolor('forestgreen')

turtleColors = ['red', 'blue', 'yellow', 'black', 'purple']
balance = 100
turtles = []
os.system('cls')

def print_turtles(color):
    if not turtleColors:
        print("No turtles")
    else:
        for i, color in enumerate(turtleColors, start=1):
            print(f"{i}. {color}")

print("=== TURTLE RACE ===")
print(f"Your starting balance: {balance} shells")
print("Available turtles:")
print_turtles(color)
while True:
    betColor = textinput("Place Bet", "which turtle do you want to bet on? ").strip().lower()
    if betColor in turtleColors:
        break
    print("Turtle not available. Please choose from the list.")
    print_turtles(color)

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
print(f"You bet {betAmount} shells on the {betColor} turtle. Good luck!")
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
betDisplay.write(f"Your bet: {betAmount} shells on {betColor} | Balance: {balance} shells", align="center", font=("Arial", 16, "normal"))

for paint in turtleColors:
    racer = Turtle(shape='turtle')
    racer.color(paint)
    racer.penup()
    racer.goto(-200, (turtleColors.index(paint) * 40) - 80)
    turtles.append(racer)

winner = None
while not winner:
    for racer in turtles:
        racer.forward(random.randint(1, 10))
        if racer.xcor() >= 200:
            winner = racer.pencolor()
            break

print(f"The winner is the {winner} turtle!")
if betColor == winner:
    winnings = betAmount * 4
    balance += winnings
    resultMessage = f"\nCongratulations! You won {winnings} shells.\nYour new balance is {balance} shells."
    print(resultMessage)

else:
    resultMessage = f"\nSorry, you lost your bet.\nYour new balance is {balance} shells."
    print(resultMessage)
    if balance == 0:
        time.sleep(2.5)
        os.system('cls')
        sys.exit()

resultDisplay = Turtle()
resultDisplay.hideturtle()
resultDisplay.penup()
resultDisplay.color('white')
resultDisplay.goto(0, -200)
resultDisplay.write(resultMessage, align="center", font=("Arial", 16, "normal"))

done()