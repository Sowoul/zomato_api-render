from urllib.request import Request, urlopen
import re

def scrape(city):
    temp = urlopen(Request(f"https://www.zomato.com/{city}/restaurants?rating_range=3.7-5.0&category=1", headers={'User-Agent': 'Mozilla/5.0'})).read().decode("utf-8")
    part = """"@type":"Thing","name":"""
    rests = re.split(part, temp)
    
    restaurant_data = []
    
    for i in range(len(rests)):
        if i > 0:
            name = rests[i].split('","')[0].strip('"')
            image_link = rests[i].split(',"image":"')[1].split('"')[0].strip('"')
            restaurant_data.append((name, image_link))
    
    return restaurant_data

if __name__ == '__main__':
    city = "udaipur"
    restaurants = scrape(city)
    for name, image_link in restaurants:
        print(f"{name}: {image_link}")
