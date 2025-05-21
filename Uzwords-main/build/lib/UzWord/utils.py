import re
import unicodedata

def normalize_apostrophe(word):
    """Apostroflarni (' va ‘), qo'shtirnoqlarni ("), va backtick (`) standartlashtiradi."""
    word = unicodedata.normalize('NFKC', word)
    return word.replace('\'', "‘").replace('"', "‘").replace('`', "‘")

def is_valid_uzbek_word(word):
    """
    So‘zning o‘zbek tiliga mosligini tekshiradi:
    - O‘zbek harflari, ch, sh, apostrof (‘) va qisqartmalar qabul qilinadi.
    - Raqamlar va maxsus belgilar filtrlanadi.
    """
    word = normalize_apostrophe(word)
    if any(char.isdigit() for char in word) or word.startswith("'") or len(word) <= 2:
        return False
    pattern = r'^[a-zA-Z\'chsh]+$'
    return bool(re.match(pattern, word, re.UNICODE))

def extract_words(text):
    """Matndan o‘zbek tiliga mos so‘zlarni ajratib oladi."""
    text = normalize_apostrophe(text)
    words = re.findall(r'\b[a-zA-Z\'chsh]+\b', text, re.UNICODE)
    return [word.lower() for word in words if word and is_valid_uzbek_word(word)]

def get_first_letter(word):
    """So‘zning birinchi harfini qaytaradi, o‘zbek alifbosiga mos ravishda."""
    word = word.lower().strip()
    if not word:
        return None
    if word.startswith("o'"):
        return "o'"
    if word.startswith("g'"):
        return "g'"
    if word.startswith('sh'):
        return 'sh'
    if word.startswith('ch'):
        return 'ch'
    if word.startswith('ng'):
        return 'ng'
    return word[0]
def levenshtein_distance(s1, s2):
    """Ikki so‘z o‘rtasidagi Levenshtein masofasini hisoblaydi."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def find_closest_word(word, dictionary):
    """Lug‘atdagi eng yaqin so‘zni topadi."""
    if word in dictionary:
        return word
    return min(dictionary, key=lambda x: levenshtein_distance(word, x))