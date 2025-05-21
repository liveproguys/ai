from UzWord import Database

def main():
    db = Database()
    file_path = r"C:\Users\jahongir\Desktop\Ai\Uzwords-main\data\wordlist.txt"
    wordlist = db.get_wordlist(file_path)
    print(f"Mavjud so‘zlar soni: {len(wordlist)}")

    print("Matnni kiriting (chiqish uchun 'exit' deb yozing):")
    while True:
        text = input("> ")
        if text.lower() == 'exit':
            break
        new_words = db.add_words_from_text(text, file_path)
        if new_words:
            print(f"Yangi so‘zlar qo‘shildi: {new_words}")
            wordlist.update(new_words)
        else:
            print("Yangi so‘z topilmadi.")

if __name__ == "__main__":
    main()