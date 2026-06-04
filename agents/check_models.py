import os
import json
import urllib.request
from dotenv import load_dotenv

# .env file load kar rahe hain
load_dotenv("../backend/.env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key nahi mili!")
else:
    print("⏳ Google se available models ki list mangwa rahe hain...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        # Direct Google API ko request bhej rahe hain
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            print("\n✅ Aapki API key par yeh Text/Chat models available hain:\n")
            print("-" * 40)
            
            # Sirf unhi models ko print karenge jo text generate kar sakte hain
            for model in data.get('models', []):
                if 'generateContent' in model.get('supportedGenerationMethods', []):
                    # 'models/' prefix hata kar sirf main naam print kar rahe hain
                    model_name = model.get('name').replace('models/', '')
                    print(f"👉 {model_name}")
            
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error aayi: {e}")