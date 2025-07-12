import os

info_dict = {
    #  'key' : ['file', 'title', [strings for use in messages]]
    'food': ["food_list.txt", "📋 รายการอาหาร", ["เมนู", "🍴"], 0xFFC0CB],
    'movie': ["movie_list.txt", "🍿 รายการหนัง", ["เรื่อง", "📽️"], 0xff0000],
    'restaurant': ["restaurant_list.txt", "🍽️ รายการร้านอาหาร", ["ร้าน", "🫕"], 0xFFC0CB]
}


def read_item_list(listFile):
  if not os.path.exists(listFile):
    return []
  with open(listFile, "r", encoding="utf-8") as f:
    return [line.strip() for line in f if line.strip()]


def save_item_list(file, itemList):
  with open(file, "w", encoding="utf-8") as f:
    f.write("\n".join(itemList) + "\n")
