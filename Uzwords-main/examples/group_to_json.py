import os
from UzWord import Database

def main():
    # Loyiha ildiziga nisbatan yo‘l
    project_root = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(project_root, "data", "wordlist.txt")
    output_file = os.path.join(project_root, "data", "wordlist_by_letter.json")
    
    db = Database()
    try:
        grouped = db.group_to_single_json(input_file, output_file)
        print(f"So‘zlar harf bo‘yicha guruhlanib, {output_file} ga saqlandi.")
        for letter, words in grouped.items():
            print(f"{letter}: {words['count']} ta so‘z")
    except Exception as e:
        print(f"Xato yuz berdi: {e}")

if __name__ == "__main__":
    main()