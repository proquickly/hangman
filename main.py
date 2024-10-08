import random
import string

import kivy
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from words import WORDS

# try downloading words from https://github.com/Xethron/Hangman/blob/master/words.txt
# use requests module to download


kivy.require("1.9.0")


class ButtonsLayout(GridLayout):
    INSTANCES = []

    def __init__(self, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)
        ButtonsLayout.INSTANCES.append(self)
        self.rows = 2
        self.cols = 13
        self.buttons = {}
        self.create_buttons()

    def create_buttons(self):
        for alphabet in string.ascii_uppercase:
            button = Button(
                text=alphabet,
                font_name="fonts/Plaguard.otf",
                font_size=24,
            )

            self.add_widget(button)
            self.buttons[alphabet] = button


class MyRoot(BoxLayout):
    ERRORS = StringProperty()
    HANGMAN_IMG = StringProperty()
    GAME_MSG = StringProperty()
    WORD_DISPLAY = StringProperty()

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
        self.RANDOM_WORD = ""
        self.GUESSES = []
        self.buttons_layout = ButtonsLayout.INSTANCES[0]
        self.configure_buttons()
        self.start_game()

    @property
    def won(self):
        return all(alphabet in self.GUESSES for alphabet in self.RANDOM_WORD)

    def update_word_display(self):
        WORD_DISPLAY = []
        for alphabet in self.RANDOM_WORD:
            if alphabet in self.GUESSES:
                WORD_DISPLAY.append(alphabet)
            else:
                WORD_DISPLAY.append("_")

        self.WORD_DISPLAY = " ".join(WORD_DISPLAY)

    def btn_press(self, widget):
        widget.disabled = True
        self.GUESSES.append(widget.text)

        if widget.text in self.RANDOM_WORD:
            self.update_word_display()

            if self.won:
                for button in self.buttons_layout.buttons.values():
                    button.disabled = True
                self.GAME_MSG = "You Won!!!"
        else:
            self.ERRORS = str(int(self.ERRORS) + 1)
            self.HANGMAN_IMG = "images/hangman" + self.ERRORS + ".png"
            if int(self.ERRORS) == 7:
                for button in self.buttons_layout.buttons.values():
                    button.disabled = True

                self.GAME_MSG = "GAME OVER!!!"
                self.WORD_DISPLAY = self.RANDOM_WORD

    def configure_buttons(self):
        for button in self.buttons_layout.buttons.values():
            button.on_press = lambda btn=button: self.btn_press(btn)

    def start_game(self):
        self.RANDOM_WORD = random.choice(WORDS)
        self.GUESSES.clear()
        self.ERRORS = "0"
        self.HANGMAN_IMG = "images/hangman0.png"
        self.GAME_MSG = "Guess the word"
        self.WORD_DISPLAY = " ".join(["_" for _ in self.RANDOM_WORD])
        for button in self.buttons_layout.buttons.values():
            button.disabled = False


class Hangman(App):
    def build(self):
        return MyRoot()


hangman = Hangman()
hangman.run()
