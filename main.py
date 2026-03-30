# Turtle Racing game
from turtle import *
import time
import random
# set up
hideturtle()
screen = Screen()
screen.setup(width=500, height=500)
title("Turtle Race")
bgcolor('forestgreen')
speed('fastest')

# draw lanes for turtles

# draw finish line as a checkered pattern

# create turtles
colors = ['red', 'blue', 'yellow', 'orange', 'purple']
turtles = []
for color in colors:
    racer = Turtle(shape='turtle')
    racer.color(color)
    racer.penup()
    racer.goto(-200, colors.index(color) * 40 - 80)
    turtles.append(racer)
# race
winner = None
while not winner:
    for t in turtles:
        t.forward(random.randint(1, 10))
        if t.xcor() >= 200:
            winner = t.pencolor()
            break
# announce winner
time.sleep(1)
print(f"The winner is the {winner} turtle!")
# keep window open
done()