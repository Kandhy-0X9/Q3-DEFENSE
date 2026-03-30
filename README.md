Turtle Racing game with betting mechanics.

Features:
    Betting system — You start with a $100 balance and place a bet on one of 5 colored turtles (red, blue, yellow, black, purple)
    Race visualization — Uses Python's turtle graphics to display 5 lanes with a finish line
    Racing logic — Turtles move forward by random amounts (1-10 pixels) until one reaches the finish line at x=200
    Payout — If your turtle wins, you get 4x your bet amount; if you lose, you lose your bet amount

Main flow:
    Display intro and available turtles
    Prompt for turtle selection and bet amount validation
    Draw racing lanes and finish line
    Display betting info on screen
    Run the race (each turtle moves randomly forward)
    Announce winner and calculate final balance
    Display result on screen