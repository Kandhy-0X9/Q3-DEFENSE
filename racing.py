# Turtle Racing game with Betting
from turtle import *
import random
import os

# Set up window
hideturtle()
screen = Screen()
screen.setup(width=500, height=500)
title("Turtle Race")

turtleColors = ['red', 'blue', 'yellow', 'black', 'purple']
balance = 100
os.system('cls')  # Clear console for better readability

def print_turtles():
    for i, color in enumerate(turtleColors, start=1):
        print(f"{i}. {color}")

def reset_track():
    """Clear all turtles and drawings from the screen, keeping the window open."""
    clearscreen()
    bgcolor('forestgreen')
    title("Turtle Race")

def draw_track():
    """Draw the lanes and finish line."""
    num_lanes = 5
    laneHeight = 40
    startY = -80

    lane = Turtle()
    lane.hideturtle()
    lane.penup()
    lane.color('black')
    lane.pensize(1)
    lane.speed('fastest')

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

    return startY, laneHeight

def run_race(betColor, betAmount, balance):
    """Set up and run a single race. Returns the winner color."""
    startY, laneHeight = draw_track()

    # Display betting info
    betDisplay = Turtle()
    betDisplay.hideturtle()
    betDisplay.penup()
    betDisplay.color('white')
    betDisplay.goto(0, 200)
    betDisplay.write(
        f"Your bet: {betAmount} shells on {betColor} | Balance: {balance} shells",
        align="center", font=("Arial", 16, "normal")
    )

    # Place turtles on the track
    turtles = []
    for paint in turtleColors:
        racer = Turtle(shape='turtle')
        racer.color(paint)
        racer.penup()
        racer.goto(-200, (turtleColors.index(paint) * 40) - 80)
        turtles.append(racer)

    # Race loop
    winner = None
    while not winner:
        for racer in turtles:
            racer.forward(random.randint(1, 10))
            if racer.xcor() >= 200:
                winner = racer.pencolor()
                break

    return winner

def show_result(resultMessage):
    """Display the result message on screen."""
    resultDisplay = Turtle()
    resultDisplay.hideturtle()
    resultDisplay.penup()
    resultDisplay.color('white')
    resultDisplay.goto(0, -200)
    resultDisplay.write(resultMessage, align="center", font=("Arial", 16, "normal"))

# ── Main game loop ──────────────────────────────────────────────────────────────
print("=== TURTLE RACE ===")
print(f"Your starting balance: {balance} shells")

while balance > 0:
    os.system('cls')
    print("=== TURTLE RACE ===")
    print(f"Current balance: {balance} shells")
    print("Available turtles:")
    print_turtles()

    reset_track()

    # Get bet color
    while True:
        betColor = textinput("Place Bet", "Which turtle do you want to bet on?").strip().lower()
        if betColor in turtleColors:
            break
        print("Turtle not available. Please choose from the list.")
        print_turtles()

    # Get bet amount
    while True:
        try:
            betAmount = int(textinput("Bet Amount", f"How much do you want to bet? (max {balance} shells)"))
            if 0 < betAmount <= balance:
                break
            else:
                print(f"Please enter an amount between 1 and {balance} shells.")
        except (ValueError, TypeError):
            print("Invalid input. Please enter a whole number.")

    balance -= betAmount
    print(f"\nYou bet {betAmount} shells on the {betColor} turtle. Good luck!")
    print("Starting race...\n")

    # Run the race
    winner = run_race(betColor, betAmount, balance)
    print(f"The winner is the {winner} turtle!")

    # Settle the bet
    if betColor == winner:
        winnings = betAmount * 4
        balance += winnings
        resultMessage = f"Congratulations! You won {winnings} shells.\nYour new balance is {balance} shells."
    else:
        resultMessage = f"Sorry, you lost your bet.\nYour new balance is {balance} shells."

    print(resultMessage)
    show_result(resultMessage)

    # Out of money — game over
    if balance <= 0:
        print("\nYou're out of money! Game over.")
        textinput("Game Over", "You're out of money! Press OK to exit.")
        break

    # Ask to play again
    again = textinput("Play Again?", f"Balance: {balance} shells. Play another race? (yes/no)").strip().lower()
    if again != 'yes':
        print(f"\nThanks for playing! You finished with {balance} shells.")
        break

done()