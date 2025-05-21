from UzWord import Database

def main():
    db = Database()
    
    # So‘zlarni o‘qish
    words = db.get_wordlist("data/wordlist.txt")
    print(f"Jami so‘zlar: {len(words)}")

    # Harflarga guruhlash
    grouped = db.group_by_letter(words)
    print("So‘zlar harflarga guruhlandi.")

    # Statistikani ko‘rsatish
    stats = db.get_letter_stats(words)
    for letter, count in stats.items():
        print(f"{letter}: {count} ta so‘z")

if __name__ == "__main__":
    main()