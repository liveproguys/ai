import google.generativeai as genai

genai.configure(api_key="AIzaSyDJTmtsV6SxsB1uPj-y1746ON2HOrKb16Q")

def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini xatolik:", e)
        return "Kechirasiz, men bu haqida bilmayman."