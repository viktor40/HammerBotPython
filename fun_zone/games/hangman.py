import random

import fun_zone.games.hangman_data as data


class Hangman:
    """Handles all game related actions for hangman

    Attributes:
        word -- the word to be guessed
        tries -- the number of tries left
        word_completion -- the representation of the hangman word
        guessed_letters -- a list containing all previously guessed letters
        guessed_words -- a list containing all previously guessed words
        hangman -- the hangman character art in it's current stages
    """

    def __init__(self):
        self.word = None
        self.tries = len(data.stages)
        self.word_completion = None
        self.guessed_letters = None
        self.guessed_words = None
        self.hangman = None

    def start(self):
        """
        This will initialise a hangman game and generate the necessary data.

        :return: The message to be sent to discord.
        """

        self.tries = len(data.stages)
        self.word = get_word()
        self.word_completion = "\\_ " * len(self.word)
        self.guessed_letters = []
        self.guessed_words = []
        return ("Thanks for playing hangman. Try to guess this {} letter word. You have {} tries left"
                "\n\n{}".format(len(self.word),
                                self.tries,
                                self.word_completion
                                )
                )

    def guess_letter(self, letter):
        """
        This will handle guessing letters. We check for letters that have already been guessed.
        :param letter: The letter that is being guessed.
        :return: The message to be sent to discord.
        """

        if letter in self.guessed_letters:
            return "You have already guessed the letter {}.".format(letter)

        elif letter not in self.word:
            self.tries -= 1
            self.hangman = data.stages[self.tries]
            self.guessed_letters.append(letter)

            if self.tries != 0:
                return ("The letter {} is not in the word. Please try again. You have {} tries left."
                        "\n{}\n\n{}".format(letter,
                                            self.tries,
                                            self.hangman,
                                            self.word_completion)
                        )
            else:
                return ("The letter {} is not in the word. Please try again. You have {} tries left.\n"
                        "The game is over, you didn't guess the correct word. Also why did you guess a letter"
                        "as your last try. The correct word is {}"
                        "\n{}\n\n{}".format(letter,
                                            self.tries,
                                            self.word,
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
            if self.word_completion.replace(" ", "") == self.word:
                return ("Congratulations, the letter {} was in the word.\n"
                        "You won the game. The correct word was indeed {}.\n"
                        "You won after {} tries".format(letter,
                                                        self.word,
                                                        9 - self.tries)
                        )
            else:
                return ("Congratulations, the letter {} was in the word."
                        "You have {} tries left.\n\n{}".format(letter,
                                                               self.tries,
                                                               self.word_completion)
                        )

    def guess_word(self, word):
        """
        This will handle guessing words. We check for words that have already been guessed.

        :param word: The word that is being guessed.
        :return: The message to be sent to discord.
        """

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
            if self.tries != 0:
                return ("You guessed the word {}. This is incorrect. Please try again. You have {} tries left."
                        "\n{}\n\n{}".format(word,
                                            self.tries,
                                            self.hangman,
                                            self.word_completion)
                        )
            else:
                return ("You guessed the word {}. This is incorrect. Please try again. You have {} tries left.\n"
                        "The game is over. The correct word was {}"
                        "\n{}\n\n{}".format(word,
                                            self.tries,
                                            self.word,
                                            self.hangman,
                                            self.word_completion)
                        )


def get_word():
    """
    :return: a random word from fun_zone.games.hangman_data.word_list
    """
    word = random.choice(data.word_list)
    return word.upper()
