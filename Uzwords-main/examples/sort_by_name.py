
def sort_wordlist(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            words = file.readlines()
        
        words = [word.strip() for word in words if word.strip()]
        
        sorted_words = sorted(words, key=lambda x: x.lower())  # Katta-kichik harfni hisobga olmaslik uchun
        
        with open(output_file, 'w', encoding='utf-8') as file:
            for word in sorted_words:
                file.write(word + '\n')
        
        print(f"So'zlar alifbo tartibida saralndi va {output_file} fayliga saqlandi.")
    
    except FileNotFoundError:
        print("Xato: Kirish fayli topilmadi.")
    except Exception as e:
        print(f"Xato yuz berdi: {e}")

input_file = "wordlist.txt"
output_file = "sorted_wordlist.txt"

sort_wordlist(input_file, output_file)