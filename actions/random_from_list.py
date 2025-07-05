from . import common_action_util as cau
import random

FOOD_FILE = "food_list.txt"

def rand_action(Msg):
    if Msg == "!randfood":
        return random_food_from_list()
    elif Msg == "!randmovie":
        return random_movie_from_list()

def random_food_from_list():
    food_list = cau.read_item_list(FOOD_FILE)
    if not food_list:
        return "ยังไม่มีเมนูอาหารในรายการเลย ลองเพิ่มก่อนสิ!"
    else:
        food = random.choice(food_list)
        return f"สุ่มได้เมนู: **{food}** 🍽️"

def random_movie_from_list():
    return "สุ่มได้หนัง: **The Matrix** 🍿"