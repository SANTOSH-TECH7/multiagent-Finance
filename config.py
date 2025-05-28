import google.generativeai as genai

class Config:
    def __init__(self):
        self.gemini_key = None
        self.model = None

    def setup_gemini(self, api_key):
        self.gemini_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        return True