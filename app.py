from flask import Flask, render_template, request
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        price_range = request.form['price_range']
        df = generate_csv(price_range)
        return render_template('results.html', data=df.to_dict('records'))
    return render_template('index.html')

def generate_csv(price_range):
    Product_name = []
    Prices = []
    Description = []
    Reviews = []

    for i in range(1, 2):
        url = f"https://www.flipkart.com/search?q=mobile+phones+under+{price_range}&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_5_0_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_5_0_na_na_na&as-pos=5&as-type=HISTORY&suggestionId=mobile+phones+under+{price_range}&requestId=5e849315-c609-4058-bf07-aba461c9d306&page={i}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        box = soup.find("div", class_="_1YokD2 _3Mn1Gg")
        names = box.find_all("div", class_="_4rR01T")

        for i in names:
            name = i.text
            Product_name.append(name)

        prices = box.find_all("div", class_="_30jeq3 _1_WHN1")
        for i in prices:
            name = i.text
            Prices.append(name)

        desc = box.find_all("ul", class_="_1xgFaf")
        for i in desc:
            name = i.text
            Description.append(name)

        reviews = box.find_all("div", class_="_3LWZlK")
        for i in reviews:
            name = i.text
            Reviews.append(name)

    df = pd.DataFrame(
        {
            "Product Name": Product_name,
            "Prices": Prices,
            "Description": Description,
            "Reviews": Reviews,
        }
    )
    return df

if __name__ == '__main__':
    app.run()
