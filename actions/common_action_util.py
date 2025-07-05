import os

def read_item_list(listFile):
  if not os.path.exists(listFile):
    return []
  with open(listFile, "r", encoding="utf-8") as f:
    return [line.strip() for line in f if line.strip()]

def save_item_list(file,itemList):
  with open(file, "w", encoding="utf-8") as f:
      f.write("\n".join(itemList) + "\n")