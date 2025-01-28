import google.generativeai as genai
genai.configure(api_key="AIzaSyDGcXW3GY6_IGBXAEjieryd0OMkZwrsm58")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)