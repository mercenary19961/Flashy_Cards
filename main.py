from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


# ---------------------------- PICKING RANDOM WORD ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/russian_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- Buttons functionality ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(title_text, text="Russian", fill="black")
    canvas.itemconfig(word_text, text=current_card["Russian"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.minsize(width=500, height=400)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 48, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

canvas.grid(row=0, column=1, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

unknown_button_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_button_img, command=next_card, highlightthickness=0)
unknown_button.grid(row=1, column=1)

known_button_img = PhotoImage(file="images/right.png")
known_button = Button(image=known_button_img, command=is_known, highlightthickness=0)
known_button.grid(row=1, column=2)

next_card()

window.mainloop()
