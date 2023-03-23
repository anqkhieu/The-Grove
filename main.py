import os, json, requests
from dotenv import load_dotenv

load_dotenv()
BLOCKADE_API_KEY = os.getenv('BLOCKADE_API_KEY')
MAGICSAUCE_USER_ID = os.getenv('MAGICSAUCE_USER_ID')
MAGICSAUCE_API_KEY = os.getenv('MAGICSAUCE_API_KEY')

def auth(customer_id, api_key):
    try:
        credentials = {
            'customer_id': customer_id,
            'api_key': api_key
        }
        response = requests.post('https://api.applymagicsauce.com/auth', json=credentials)
        response.raise_for_status()
        return response.json()['token']
    except requests.exceptions.HTTPError as e:
        print(e.response.json())


def predict_from_text(token, text):
    try:
        response = requests.post(url='https://api.applymagicsauce.com/text',
                                 data=text.encode('utf-8'),
                                 headers={'X-Auth-Token': token})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(e.response.json())


def predict_from_like_ids(token, like_ids):
    try:
        response = requests.post(url='https://api.applymagicsauce.com/like_ids',
                                 json=like_ids,
                                 headers={'X-Auth-Token': token})
        response.raise_for_status()
        if response.status_code == 204:
            raise ValueError('Not enough predictive like ids provided to make a prediction')
        else:
            return response.json()
    except requests.exceptions.HTTPError as e:
        print(e.response.json())
    except ValueError as e:
        print(e)


def predict_from_like_names(token, like_names):
    try:
        response = requests.post(url='https://api.applymagicsauce.com/like_names',
                                 json=like_names,
                                 headers={'X-Auth-Token': token})
        response.raise_for_status()
        if response.status_code == 204:
            raise ValueError('Not enough predictive names provided to make a prediction')
        else:
            return response.json()
    except requests.exceptions.HTTPError as e:
        print(e.response.json())
    except ValueError as e:
        print(e)


def predict(customer_id, api_key):
    token = auth(customer_id, api_key)
    prediction_result = predict_from_text(token, 'Lorem ipsum dolor sit amet')
    print(json.dumps(prediction_result, indent=4))
    return prediction_result
  
  
profile = predict(MAGICSAUCE_USER_ID, MAGICSAUCE_API_KEY)


# Then, use profile data to comeup with traits to input into Blockade API to generate world of interest
def blockade_gen(prompt):
    url = f"https://backend.blockadelabs.com/api/v1/imagine/requests?api_key={BLOCKADE_API_KEY}"
    form_data = {
        'prompt': prompt, 
        'generator': 'stable-skybox',
        'animation_mode': 'skybox',
        'negative_text': 'blurry, lowres, text, error, worst quality, low quality, bad quality'
    }
    requests.post(url, headers={"Content-Type": "application/json"}, json = form_data)
