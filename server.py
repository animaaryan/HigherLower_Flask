from flask import Flask
from random import randint

app = Flask(__name__)

START_GIF = 'https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'

RIGHT_ANSWER = "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"

HIGHER_GIF = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"

LOWER_GIF = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"

LOSER_GIF = "https://media.giphy.com/media/OzlmyoTC2n3aOTXGFi/giphy.gif"

MAX_GUESSES = 5
guesses_left = MAX_GUESSES
RANDOM_NUMBER = randint(1, 9)


def style_decorator(base_fn):
    def wrapper(**kwargs):
        text = base_fn(**kwargs)
        if base_fn.__name__ == 'right_guess':
            if 'low' in text:
                text_color = 'red'
                text_align = 'center'
                gif_link = LOWER_GIF
            elif 'high' in text:
                text_color = 'purple'
                text_align = 'center'
                gif_link = HIGHER_GIF
            elif 'out' in text:
                text_color = 'red'
                text_align = 'center'
                gif_link = LOSER_GIF
            else:
                text_color = 'green'
                text_align = 'center'
                gif_link = RIGHT_ANSWER
        else:
            text_color = 'black'
            text_align = 'center'
            gif_link = START_GIF
        return (f'<h1 style="color:{text_color}; text-align:{text_align}">{text}</h1><br><br>'
                f'<img style="display:block; margin:auto; border-radius:12px;" src="{gif_link}">')

    return wrapper


@app.route("/", endpoint="begin")
@style_decorator
def welcome():
    global guesses_left, RANDOM_NUMBER
    guesses_left = MAX_GUESSES
    RANDOM_NUMBER = randint(1, 9)
    return 'Guess a number between 0 and 9'


@app.route("/<int:guess>", endpoint="guess")
@style_decorator
def right_guess(guess):
    global guesses_left

    if guesses_left < 1:
        text = f"You're out of guesses! It was {RANDOM_NUMBER}. <p>You Lose</p>"
    elif guess > RANDOM_NUMBER:
        text = f'Too high, try again! <p> You have {guesses_left} guesses left </p>'
        guesses_left -= 1
    elif guess < RANDOM_NUMBER:
        text = f'Too low, try again! <p> You have {guesses_left} guesses left </p>'
        guesses_left -= 1
    else:
        text = 'You found me!'

    return text


if __name__ == "__main__":
    app.run(debug=True)
