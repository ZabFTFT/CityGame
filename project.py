import random
import re
import pandas
import sys
import time


URL = "https://gist.githubusercontent.com/ZabFTFT/487e75ea0b3ac161f9f248e38d2801b7/raw/e3116660dfde774cd1e583187601843e0eb2cb48/WorldCities"

# Class with reactions
class Reactions:
    """
    This class will be used for text reactions
    """
    positive_reactions = ["\n Good job! Good job! Good job!\n", "\nI accept this variant! You are good!\n", "\nYou are smart!\n", "\nNot very hard, right?\n"]
    algo_answer_reactions = ["My answer is: ", "I am gonna pick: ", "My variant is: "]
    algo_skip_reactions = ["Sometimes I can't to remember the city name aswell!\n", "Try your best with another letter!\n", "This is easier!\n"]

    @classmethod
    def positive_reaction(cls):
        return random.choice(cls.positive_reactions)

    @classmethod
    def algo_answer_reaction(cls):
         return random.choice(cls.algo_answer_reactions)

    @classmethod
    def algo_skip_reaction(cls):
         return random.choice(cls.algo_skip_reactions)
    
    @classmethod
    def algo_shortcuts(cls):
        return "Type this commands: quit - for finish programm, skip - for skip current letter, short - for display shortcuts\n"

class Score:
    """Class for tracking score value"""

    score = 0

    @classmethod
    def score_increase(cls):
        cls.score += 1

    @classmethod
    def score_display(cls):
        if cls.score >=5:
            return f"You did fantastic job! You score is {cls.score}"
        elif cls.score < 5:
            return f"\nNext time you will do a better job! You score is {cls.score}"



def main():

    # Adding data to list
    list_of_cities = create_list_of_cities()
    

    last_letter = letter_generator()
    print("Welcome to CityGame!")
    time.sleep(0)
    print("\nI'd like to introduce mechanic of the game and some shortcuts")
    time.sleep(0)
    print("\nThere is only one rule: the first letter of your answer must start with last letter of previous city")
    time.sleep(0)
    print("\nFor example: if i typed Kyiv, you need to enter the name of city with first letter V, like Vancouver")
    time.sleep(0)
    print("\nWe have some shortcuts as well to increase fun and control of process")
    time.sleep(0)
    print(f"\n{Reactions.algo_shortcuts()}")
    time.sleep(0)
    print(f"\nLets start our game with letter {last_letter}\n")

    # Main game
    while True:
        user_answer_var, last_letter = user_answer(last_letter, list_of_cities)
        Score.score_increase()
        list_of_cities.remove(user_answer_var)

        algo_answer_var, last_letter = algo_answer(last_letter, list_of_cities)
        list_of_cities.remove(algo_answer_var)
    

def letter_generator():
    alpha = "QWERTYUIOPLKJHGFDSAZXCVBNM"
    return random.choice(alpha)


def create_list_of_cities():
    city_list = []

    df = pandas.read_csv(URL)
    records = df.to_dict(orient='records')
    for element in records:
        for key, value in element.items():
            match = re.match(r"^[a-zA-Z]+(\s|-|\.)?(\s)?([a-zA-Z]+)?(\s)?([a-zA-Z]+)?", str(value))
            if key == "city" and match:
                city_list.append(value)
    return city_list


def user_answer(last_letter: str, list_of_cities: list):
    while True:
        print(f"Type city name that is start with {last_letter}")
        answer = input("Type your variant: ").strip().title()
        if answer == "Quit":
            print(Score.score_display())
            sys.exit("\nSee you again!")
        if answer == "Skip":
            last_letter = skip_function(last_letter)
            continue
        if answer == "Short":
            print(f"\n{Reactions.algo_shortcuts()}")
            continue
        match = re.match(r"^[a-zA-Z]+(\s|-|\.)?(\s)?([a-zA-Z]+)?(\s)?([a-zA-Z]+)?", answer)
        if not match:
            print("You've used unallowed symbol in the name of city. Try again!\n")
            continue
        if answer[0] != last_letter:
            print(f"First letter of your answer must be: {last_letter}\n")
            continue
        if answer not in list_of_cities:
            print("This city name doesn't exist or the name was used already. Try again!\n")
            continue

        print(Reactions.positive_reaction())
        return answer, answer[-1].upper()


def skip_function(last_letter):
    previous_variant = last_letter
    last_letter = letter_generator()
    while last_letter == previous_variant:
        last_letter = letter_generator()
    print(f"{Reactions.algo_skip_reaction()}")
    return last_letter


def algo_answer(last_letter: str, list_of_cities: list):
    for number in range(len(list_of_cities)):
        if list_of_cities[number][0] == last_letter:
            print(f"{Reactions.algo_answer_reaction()}{list_of_cities[number]}\n")
            return list_of_cities[number], list_of_cities[number][-1].upper()


if __name__ == "__main__":
    main()