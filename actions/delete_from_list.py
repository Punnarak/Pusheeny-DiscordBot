from . import common_action_util as cau

FOOD_FILE = "food_list.txt"


def delete_food(food):
    arg = food[len("!delfood "):].strip()
    food_list = cau.read_item_list(FOOD_FILE)
    if not food_list:
        return "ยังไม่มีเมนูอาหารในรายการเลย"

    # ลบตามเลขลำดับ
    if arg.isdigit():
        index = int(arg) - 1
        if 0 <= index < len(food_list):
            removed = food_list.pop(index)
            cau.save_item_list(FOOD_FILE, food_list)  # ← ใช้ฟังก์ชันใหม่
            return f"ลบเมนูลำดับ {index+1}: **{removed}** เรียบร้อยแล้ว"
        else:
            return "เลขลำดับไม่ถูกต้อง"
    else:
        # ลบตามชื่อเมนู
        if arg in food_list:
            food_list.remove(arg)
            cau.save_item_list(FOOD_FILE, food_list)  # ← ใช้ฟังก์ชันใหม่
            return f"ลบเมนู: **{arg}** เรียบร้อยแล้ว"
        else:
            return f"ไม่พบเมนูชื่อ `{arg}`"


def delete_action(command):
    if command.startswith("!delfood "):
        return delete_food(command)
    else:
        return "ไม่รู้จักคำสั่งนี้"
