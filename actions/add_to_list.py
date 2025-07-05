from . import common_action_util as cau

FOOD_FILE = "food_list.txt"

def add_item(file, item):
  with open(file, "a", encoding="utf-8") as f:
    f.write(item.strip() + "\n")

def add_food(food):
  food = food[len("!addfood "):].strip()
  if food:
    food_list = cau.read_item_list(FOOD_FILE)
    if food in food_list:
      return f"มีเมนู **{food}** อยู่ในรายการแล้ว!"
    else:
      add_item(FOOD_FILE, food)
      return f"เพิ่มเมนู: **{food}** เรียบร้อยแล้ว!"
  else:
    return "โปรดระบุชื่ออาหาร เช่น `!addfood ข้าวผัดกุ้ง`"

def add_action(command):
  if command.startswith("!addfood"):
    return add_food(command)
  else:
    return "ไม่รู้จักคำสั่งนี้"
