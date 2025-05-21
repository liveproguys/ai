from UzWord import Database

def main():
    db = Database()
    file_path = r"C:\Users\jahongir\Desktop\Ai\Uzwords-main\data\wordlist.txt"
    print("Iltimos, matn kiriting (chiqish uchun 'exit' yozing):")
    while True:
        text = input("> ")
        if text.lower() == 'exit':
            break
        corrected_text = db.correct_text(text, file_path)
        print("Tuzatilgan matn:", corrected_text)

if __name__ == "__main__":
    main()