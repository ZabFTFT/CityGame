import random
import re
import pandas
import sys


URL = "https://gist.githubusercontent.com/ZabFTFT/487e75ea0b3ac161f9f248e38d2801b7/raw/e3116660dfde774cd1e583187601843e0eb2cb48/WorldCities"

# Class with reactions
class Reactions:
    """
    This class will be used for text reactions
    """
    positive_reactions = ["\n Good job! Good job! Good job!\n", "\nI accept this variant! You are good!\n", "\nYou are smart!\n", "\nNot very hard, right?\n"]
    algo_answer_reactions = ["My answer is: ", "I am gonna pick: ", "My variant is: "]
    algo_skip_reactions = ["Sometimes I can't to remember the city name aswell!\n", "Try your best with this one!\n", "This is easier!\n"]

    @classmethod
    def positive_reaction(cls):
        return random.choice(cls.positive_reactions)

    @classmethod
    def algo_answer_reaction(cls):
         return random.choice(cls.algo_answer_reactions)

    @classmethod
    def algo_skip_reaction(cls):
         return random.choice(cls.algo_skip_reactions)




def main():

    # Adding data to list
    list_of_cities = create_list_of_cities()

    last_letter = letter_generator()
    print(f">>>Lets start our game with letter {last_letter}\n")

    # Main game
    while True:
        user_answer_var, last_letter = user_answer(last_letter, list_of_cities)
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
            sys.exit()
        if answer == "Skip":
            last_letter = skip_function(last_letter)
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