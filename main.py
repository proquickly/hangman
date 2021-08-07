# Importing the required libraries.
import random
import string

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class MainLayout(BoxLayout):
    # Errors to keep track the number of errors.
    ERRORS = StringProperty("")

    # The path to hangman image.
    HANGMAN_IMG = StringProperty("images/hangman0.png")

    # The game message "Start the Game" or "Guess
    # the Word" or "You Won" or "Game Over"
    GAME_MSG = StringProperty("Start the Game")

    # The random word place holder.
    RANDOM_WORD_DISPLAY = StringProperty()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        # Random word to be guessed.
        self.RANDOM_WORD = ""

        # List of the guesses letters.
        self.GUESSES = []

        # Dictionary of alphabets buttons.
        self.buttons = {}

    def create_buttons(self):
        # Creating a layout for the buttons.
        buttons_layout = GridLayout(rows=2, cols=13, size_hint=(1, 0.5))

        # Creating buttons for all the alphabets and
        # adding them to the layout and dictionary.
        for letter in string.ascii_uppercase:
            button = Button(text=letter, on_press=lambda btn: self.btn_click(btn))
            buttons_layout.add_widget(button)
            self.buttons[letter] = button

        # Adding layout to the main layout.
        self.add_widget(buttons_layout)

    def start_game(self, btn):
        # Change the button text to Restart.
        btn.text = "Restart"

        # Creating the buttons if it doesn't exist.
        if not self.buttons:
            self.create_buttons()

        # Getting a random word.
        self.RANDOM_WORD = random.choice(WORDS)

        # Setting guesses to empty list.
        self.GUESSES = []

        # Changing the game message.
        self.GAME_MSG = "Guess the Word"

        # Changing the image of the hangman.
        self.HANGMAN_IMG = "images/hangman0.png"

        # Changing the display of the random word.
        self.RANDOM_WORD_DISPLAY = "".join("_" for _ in str(self.RANDOM_WORD))

        # Setting errors to zero.
        self.ERRORS = "0"

        # Enabling all the buttons.
        for _, button in self.buttons.items():
            button.disabled = False

    def btn_click(self, btn):
        # Disabling the button.
        btn.disabled = True

        # Adding the letter to guesses.
        self.GUESSES.append(btn.text)

        # Checking if letter in random word.
        if btn.text in self.RANDOM_WORD:
            # Changing the display of the random word.
            self.RANDOM_WORD_DISPLAY = ""
            for letter in self.RANDOM_WORD:
                if letter not in self.GUESSES:
                    self.RANDOM_WORD_DISPLAY += "_"
                else:
                    self.RANDOM_WORD_DISPLAY += letter
        else:
            # Adding 1 to errors.
            self.ERRORS = str(int(self.ERRORS) + 1)

        # Changing the hangman image.
        self.HANGMAN_IMG = "images/hangman" + self.ERRORS + ".png"

        # Checking if errors == 7, else
        # Checking if word is guessed.
        if int(self.ERRORS) == 7:
            # Disabling the buttons.
            for _, button in self.buttons.items():
                button.disabled = True

            # Changing the game message.
            self.GAME_MSG = "GAME OVER"

            # Changing the display of the random word.
            self.RANDOM_WORD_DISPLAY = self.RANDOM_WORD
        elif self.RANDOM_WORD_DISPLAY == self.RANDOM_WORD:
            # Disabling the buttons.
            for _, button in self.buttons.items():
                button.disabled = True

            # Changing the game message.
            self.GAME_MSG = "YOU WON"


class Hangman(App):
    pass


# Loading the words.
with open("words.txt", "r") as file:
    WORDS = [word.strip() for word in file.readlines()]

# Creating the app and running it.
app = Hangman()
app.run()
