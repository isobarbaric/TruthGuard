
import requests

def generate_req(msg):
    print(requests.get(f'http://127.0.0.1:5000/pred/{msg}').json())

generate_req('https://www.who.int/news/item/02-08-2022-who-launches-appeal-to-respond-to-urgent-health-needs-in-the-greater-horn-of-africa')