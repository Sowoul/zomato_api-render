from flask import Flask, render_template, request, jsonify
from urllib.request import Request, urlopen
import re

class Scrape:
    def scrape(city):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'utf-8',
            'Connection': 'keep-alive'
        }

        temp = urlopen(Request(f"https://www.zomato.com/{city}/restaurants?rating_range=3.7-5.0&category=1", headers=headers)).read().decode("utf-8")
        part = """"@type":"Thing","name":"""
        rests = re.split(part, temp)
        
        restaurant_data = []
        
        for i in range(len(rests)):
            if i > 0:
                name = rests[i].split('","')[0].strip('"')
                image_link = rests[i].split(',"image":"')[1].split('"')[0].strip('"')
                restaurant_data.append((name, image_link))
        
        return restaurant_data

app = Flask(__name__)

def getOrDefault(city):
    if city is None:
        return "udaipur"
    else:
        return city

@app.route('/')
def index():
    city = getOrDefault(request.args.get('city'))
    data = Scrape.scrape(city)
    return render_template('index.html', data=data)

@app.route('/post', methods=['POST'])
def post():
    city = request.form['data']
    try:
        data = Scrape.scrape(city)
        response = {
            'status': 'success',
            'city': city,
            'restaurants': [{'name': name, 'image_link': image_link} for name, image_link in data]
        }
        return jsonify(response)
    except:
        response = {
           'status': 'error',
           'message': 'City not found'
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
