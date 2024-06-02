import google.generativeai as genai
from data import collect_data
from flask import jsonify
from dotenv import load_dotenv
import time
import os

load_dotenv()



genai.configure(api_key = os.getenv('GENAI_API'))

model = genai.GenerativeModel('gemini-1.0-pro-latest')

def comment_analysis(url, ID):
    
    
    response = collect_data(ID)
    p = n = u = un = 0
    for item in response:
        time.sleep(5)
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        gmResponse = model.generate_content(f"\"{comment}\" this is a comment on a youtube video (link : '{url}') based on that is this a 'positive' or 'negative' or 'neutral' comment for the creator, just answer with one of the three options, no more information no more characters please and only lower case characters")
        
        print(f"{comment}\n")
        try:
            if gmResponse.text == "positive":
                p = p + 1
            elif gmResponse.text == "negative":
                n = n + 1
            elif gmResponse.text == "neutral":
                u = u + 1
            print(gmResponse.text)
        except Exception as e:
            
            print(e)
            un = un + 1

    return [p, n, u, un]