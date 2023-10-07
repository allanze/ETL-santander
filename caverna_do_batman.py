import pandas as pd
import requests
import json
import openai

arquivo = pd.read_csv("sdw.csv")

users_ids = arquivo["UserID"].tolist()

print(users_ids)

api_url = "https://sdw-2023-prd.up.railway.app"
openai_api_key = "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"

openai.api_key = openai_api_key

def get_user(id):
    response = requests.get(f'{api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", 
        messages = [
            {
                "role": "system",
                "content": "Você é um especialista em markting bancário."
            },
            {
                "role": "user",
                "content": f"crie uma messagem para{user['name']} sobre a importancia dos investimentos, insira sempre o nome na frase (maximo de 200 caracteres)"
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')

def update_users(user): 
    response = requests.put(f"{api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False



users = [user for id in users_ids if (user := get_user(id)) is not None]


for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "description": news
    })

for user in users:
    success = update_users(user)



