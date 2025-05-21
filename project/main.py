import importlib.util
import sys
import json
import random
import os
import re
from gemini_api import ask_gemini
from pprint import pprint
file_path = r"C:\Users\jahongir\Desktop\Ai\Uzwords-main\UzWord\__init__.py"
module_name = "UzWord"
spec = importlib.util.spec_from_file_location(module_name, file_path)
uz = importlib.util.module_from_spec(spec)
sys.modules[module_name] = uz
spec.loader.exec_module(uz)

WORDLIST = r"C:\Users\jahongir\Desktop\Ai\Uzwords-main\data\wordlist.txt"
DATA_FILE = r"C:\Users\jahongir\Desktop\Ai\project\response_base.json"

def strip_markdown(text):
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def load_responses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_response(word, answer):
    responses = load_responses()
    if word in responses:
        if answer not in responses[word]:
            responses[word].append(answer)
    else:
        responses[word] = [answer]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)

def save_word(word):
    word = word.strip()
    if not word:
        return
    words = set()
    if os.path.exists(WORDLIST):
        with open(WORDLIST, "r", encoding="utf-8") as f:
            words = set(line.strip() for line in f if line.strip())
    if word not in words:
        with open(WORDLIST, "a", encoding="utf-8") as f:
            f.write(word + "\n")

def chat(user_input,ai=True):
    db = uz.Database()
    corrected = db.correct_text(user_input, WORDLIST).strip().lower()
    if ai:
        reply_raw = ask_gemini(corrected)
        reply = strip_markdown(reply_raw)
        save_response(corrected, reply)
    responses = load_responses()
    if ai or corrected in responses:
        r=responses[corrected]
        reply = random.choice(r)
    else:
        r=responses["None"]
        reply = random.choice(r)
    return {"responses":r,"read":corrected.capitalize()+". ","result":reply}

if __name__ == "__main__":
    chat()
