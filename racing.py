# Turtle Racing game with Betting
from turtle import *
import random
import os
import sqlite3

# ── Database setup ──────────────────────────────────────────────────────────────
conn = sqlite3.connect("racing.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        name TEXT PRIMARY KEY,
        balance INTEGER,
        wins INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS races (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player TEXT,
        winner TEXT,
        bet_color TEXT,
        bet_amount INTEGER,
        result TEXT,
        balance_after INTEGER
    )
""")

conn.commit()

def load_player(name):
    # Load player from DB, or create them with 100 shells if new.
    cursor.execute("SELECT balance, wins FROM players WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        print(f"Welcome back, {name}! Loaded balance: {row[0]} shells.")
        return row[0], row[1]
    else:
        cursor.execute("INSERT INTO players VALUES (?, ?, ?)", (name, 100, 0))
        conn.commit()
        print(f"New player created: {name}. Starting balance: 100 shells.")
        return 100, 0

def save_player(name, balance, wins):
    # Save current balance and wins back to DB.
    cursor.execute(
        "UPDATE players SET balance = ?, wins = ? WHERE name = ?",
        (balance, wins, name)
    )
    conn.commit()

def log_race(player, winner, betColor, betAmount, result, balanceAfter):
    # Insert a race result into the races table.
    cursor.execute(
        "INSERT INTO races (player, winner, bet_color, bet_amount, result, balance_after) VALUES (?, ?, ?, ?, ?, ?)",
        (player, winner, betColor, betAmount, result, balanceAfter)
    )
    conn.commit()

def print_history(player):
    # Print the last 5 races for this player.
    cursor.execute(
        "SELECT winner, bet_color, bet_amount, result, balance_after FROM races WHERE player = ? ORDER BY id DESC LIMIT 5",
        (player,)
    )
    rows = cursor.fetchall()
    if not rows:
        print("No race history yet.")
        return
    print("\n--- Last 5 Races ---")
    for row in rows:
        winner, betColor, betAmount, result, balanceAfter = row
        print(f"  Winner: {winner} | Your bet: {betColor} ({betAmount} shells) | {result} | Balance after: {balanceAfter}")
    print()

def print_leaderboard():
    # Print top 5 players by wins.
    cursor.execute("SELECT name, wins FROM players ORDER BY wins DESC LIMIT 5")
    rows = cursor.fetchall()
    print("\n--- Leaderboard (Top 5) ---")
    for i, (name, wins) in enumerate(rows, start=1):
        print(f"  {i}. {name} — {wins} wins")
    print()

# ── Game setup ──────────────────────────────────────────────────────────────────
hideturtle()
screen = Screen()
screen.setup(width=500, height=500)
title("Turtle Race")

turtleColors = ['red', 'blue', 'yellow', 'black', 'purple']
os.system('cls')

def print_turtles():
    for i, color in enumerate(turtleColors, start=1):
        print(f"{i}. {color}")

def reset_track():
    # Clear all turtles and drawings from the screen, keeping the window open.
    clearscreen()
    bgcolor('forestgreen')
    title("Turtle Race")

def draw_track():
    # Draw the lanes and finish line.
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
    # Set up and run a single race. Returns the winner color.
    startY, laneHeight = draw_track()

    betDisplay = Turtle()
    betDisplay.hideturtle()
    betDisplay.penup()
    betDisplay.color('white')
    betDisplay.goto(0, 200)
    betDisplay.write(
        f"Your bet: {betAmount} shells on {betColor} | Balance: {balance} shells",
        align="center", font=("Arial", 16, "normal")
    )

    turtles = []
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

    return winner

def show_result(resultMessage):
    # Display the result message on screen.
    resultDisplay = Turtle()
    resultDisplay.hideturtle()
    resultDisplay.penup()
    resultDisplay.color('white')
    resultDisplay.goto(0, -200)
    resultDisplay.write(resultMessage, align="center", font=("Arial", 16, "normal"))

# ── Main game loop ──────────────────────────────────────────────────────────────
playerName = textinput("Welcome", "Enter your name:").strip()
balance, wins = load_player(playerName)

while balance > 0:
    os.system('cls')
    print("=== TURTLE RACE ===")
    print(f"Player: {playerName} | Balance: {balance} shells | Wins: {wins}")
    print_history(playerName)
    print_leaderboard()
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

    winner = run_race(betColor, betAmount, balance)
    print(f"The winner is the {winner} turtle!")

    # Settle the bet
    if betColor == winner:
        winnings = betAmount * 4
        balance += winnings
        result = "WIN"
        wins += 1
        resultMessage = f"Congratulations! You won {winnings} shells.\nYour new balance is {balance} shells."
    else:
        result = "LOSS"
        resultMessage = f"Sorry, you lost your bet.\nYour new balance is {balance} shells."

    # Save everything to DB
    log_race(playerName, winner, betColor, betAmount, result, balance)
    save_player(playerName, balance, wins)

    print(resultMessage)
    show_result(resultMessage)

    if balance <= 0:
        print("\nYou're out of money! Game over.")
        save_player(playerName, 0, wins)
        textinput("Game Over", "You're out of money! Press OK to exit.")
        break

    again = textinput("Play Again?", f"Balance: {balance} shells. Play another race? (yes/no)").strip().lower()
    if again != 'yes':
        print(f"\nThanks for playing! You finished with {balance} shells.")
        break

conn.close()
done()