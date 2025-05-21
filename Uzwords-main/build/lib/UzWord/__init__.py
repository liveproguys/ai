import json
import os
import re
from .utils import get_first_letter, normalize_apostrophe, is_valid_uzbek_word, extract_words, levenshtein_distance, find_closest_word
from .constants import LATIN_ALPHABET

class Database:
    def get_wordlist(self, file="data/wordlist.txt"):
        """So‘zlar ro‘yxatini fayldan o‘qiydi."""
        file = os.path.normpath(file)
        try:
            with open(file, 'r', encoding='utf-8') as f:
                words = f.readlines()
            words = [word.strip() for word in words if word.strip()]
            return set(words)
        except FileNotFoundError:
            raise FileNotFoundError(f"Fayl topilmadi: {file}")
        except Exception as e:
            raise Exception(f"Xato yuz berdi: {e}")

    def sort_wordlist(self, words):
        """So‘zlarni alifbo tartibida tartiblaydi."""
        if not isinstance(words, (set, list)):
            raise ValueError("So‘zlar ro‘yxati set yoki list bo‘lishi kerak")
        try:
            return sorted(words, key=lambda x: x.lower())
        except Exception as e:
            raise Exception(f"Tartiblashda xato: {e}")

    def group_to_single_json(self, file="..data/wordlist.txt", output="..data/wordlist_by_letter.json"):
        """So‘zlarni birinchi harf bo‘yicha guruhlab, bitta JSON faylga yozadi."""
        file = os.path.normpath(file)
        output = os.path.normpath(output)
        
        words = self.get_wordlist(file)
        grouped = {letter: {"words": [], "count": 0} for letter in LATIN_ALPHABET}
        for word in words:
            first_letter = get_first_letter(word)
            if first_letter in grouped:
                grouped[first_letter]["words"].append(word)
                grouped[first_letter]["count"] += 1
        for letter in grouped:
            grouped[letter]["words"] = self.sort_wordlist(grouped[letter]["words"])
        try:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(grouped, f, ensure_ascii=False, indent=2)
            return grouped
        except Exception as e:
            raise Exception(f"Faylga yozishda xato: {output}, Xato: {e}")

    def txt_to_json_by_name(self, file="..data/wordlist.txt", output="..data/sorted_by_name.json"):
        """So‘zlarni tartiblab JSON faylga yozadi."""
        file = os.path.normpath(file)
        output = os.path.normpath(output)
        words = self.get_wordlist(file)
        sorted_list = self.sort_wordlist(words)
        try:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(sorted_list, f, ensure_ascii=False, indent=2)
            return sorted_list
        except Exception as e:
            raise Exception(f"JSON yozishda xato: {e}")

    def get_letter_stats(self, words):
        """Har bir harfdan qancha so‘z borligini hisoblaydi."""
        stats = {letter: 0 for letter in LATIN_ALPHABET}
        for word in words:
            first_letter = get_first_letter(word)
            if first_letter in stats:
                stats[first_letter] += 1
        return stats

    def add_words_from_text(self, text, file="..data/wordlist.txt"):
        """Matndan o‘zbek tiliga mos so‘zlarni ajratib, faylga qo‘shadi."""
        file = os.path.normpath(file)
        words = self.get_wordlist(file)
        new_words = extract_words(text)
        unique_new_words = set(new_words) - words
        if unique_new_words:
            try:
                with open(file, 'a', encoding='utf-8') as f:
                    for word in unique_new_words:
                        f.write(word + '\n')
                return unique_new_words
            except Exception as e:
                raise Exception(f"Faylga yozishda xato: {e}")
        return set()

    def correct_text(self, text, file="..data/wordlist.txt"):
        """Matndagi so‘zlarni lug‘at asosida tuzatadi."""
        file = os.path.normpath(file)
        dictionary = self.get_wordlist(file)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        corrected_sentences = []
        
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            corrected_words = []
            for word in words:
                if word.isdigit():
                    corrected_words.append(word)
                else:
                    corrected_words.append(find_closest_word(word, dictionary))
            
            corrected_sentence = sentence
            for original, corrected in zip(words, corrected_words):
                if original != corrected:
                    corrected_sentence = re.sub(
                        r'\b' + original + r'\b', 
                        corrected, 
                        corrected_sentence, 
                        flags=re.IGNORECASE
                    )
            corrected_sentences.append(corrected_sentence.capitalize() + '.')
        
        return ' '.join(corrected_sentences)