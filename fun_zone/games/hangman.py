import random

import fun_zone.games.hangman_data as data


class Hangman:
    def __init__(self):
        self.word = None
        self.tries = len(data.stages)
        self.word_completion = None
        self.guessed_letters = None
        self.guessed_words = None
        self.hangman = None

    def start(self):
        self.tries = len(data.stages)
        self.word = get_word()
        self.word_completion = "\\_ " * len(self.word)
        self.guessed_letters = []
        self.guessed_words = []
        print(self.word)
        print(self.word_completion)
        return ("Thanks for playing hangman. Try to guess this {} letter word. You have {} tries left"
                "\n\n{}".format(len(self.word),
                                self.tries,
                                self.word_completion
                                )
                )

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return "You have already guessed the letter {}.".format(letter)

        elif letter not in self.word:
            self.tries -= 1
            self.hangman = data.stages[self.tries]
            self.guessed_letters.append(letter)
            return ("The letter {} is not in the word. Please try again. You have {} tries left."
                    "\n{}\n\n{}".format(letter,
                                        self.tries,
                                        self.hangman,
                                        self.word_completion)
                    )
        else:
            self.guessed_letters.append(letter)
            word_list = self.word_completion.split(" ")
            indices = [i for i, j in enumerate(self.word) if j == letter]
            for index in indices:
                word_list[index] = letter
            self.word_completion = " ".join(word_list)
            return ("Congratulations, the letter {} was in the word."
                    "You have {} tries left.\n\n{}".format(letter,
                                                           self.tries,
                                                           self.word_completion)
                    )

    def guess_word(self, word):
        if word in self.guessed_words:
            return "You have already guessed the letter {}.".format(word)

        elif word == self.word:
            result = ("Congratulations, you won. The correct word was indeed {}.\n"
                      "You solved it with {} tries".format(self.word,
                                                           9 - self.tries))
            self.word = None
            self.word_completion = None
            self.guessed_letters = None
            self.guessed_words = None
            self.hangman = None
            return result

        else:
            self.tries -= 1
            self.hangman = data.stages[self.tries]
            self.guessed_words.append(word)
            return ("You guessed the word {}. This is incorrect. Please try again. You have {} tries left."
                    "\n{}\n\n{}".format(word,
                                        self.tries,
                                        self.hangman,
                                        self.word_completion)
                    )


def get_word():
    word = random.choice(data.word_list)
    return word.upper()
