from . import common_action_util as cau

FOOD_FILE = "food_list.txt"

def get_list_action(Msg):
    if Msg == "!listfood":
        return get_food_from_list()
    elif Msg == "!randmovie":
        return random_movie_from_list()

def get_food_from_list():
    food_list = cau.read_item_list(FOOD_FILE)
    if not food_list:
        return "ยังไม่มีเมนูอาหารในรายการเลย"
    else:
        msg = "\n".join(f"{i+1}. {item}" for i, item in enumerate(food_list))
        # ถ้าข้อความยาวเกินไป อาจต้องแบ่งส่งหลายข้อความ
        if len(msg) > 1900:
            temp_return_list = list()
            for i in range(0, len(msg), 1900):
                temp_return_list.append(f"```{msg[i:i+1900]}```")
            return temp_return_list
        else:
            return [f"📋 รายการอาหาร:\n```{msg}```"]

def random_movie_from_list():
    return "สุ่มได้หนัง: **The Matrix** 🍿"



    
        