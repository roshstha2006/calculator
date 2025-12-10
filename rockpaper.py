import random

choices = ["rock","paper","scissors"]
user = input("rock/paper/scissors: ").lower()
bot = random.choice(choices)

print("Bot chose:", bot)

if user==bot:
    print("Draw!")
elif (user=="rock" and bot=="scissors") or (user=="paper" and bot=="rock") or (user=="scissors" and bot=="paper"):
    print("You Win! 🎉")
else:
    print("You Lose 😢")
