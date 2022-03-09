import requests
from bs4 import BeautifulSoup
from csv import writer
import pandas as pd
import json
import mysql.connector


def url_generator():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="flipkart152",
        database="amazon_database"
    )

    mycursor = mydb.cursor()

    mycursor.execute(
        "CREATE TABLE amazon_product (title VARCHAR(255), image VARCHAR(255), price VARCHAR(255), details VARCHAR(255))")

    df = pd.read_excel(r"C:/Users/Nakul Dalal/Desktop/amazon/coprd.xlsx",
                       sheet_name="Sheet1")
    list = []
    db = []

    for row in df.itertuples():
        asin = getattr(row, "Asin")
        country = getattr(row, "country")

        url = "https://www.amazon.{}/dp/{}"
        url = url.format(country, asin)
        print(url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        print(response)
        status_code = response.status_code
        if status_code == 200:

            soup = BeautifulSoup(response.content, "html.parser")

            try:
                title = soup.find('span', {'id': 'productTitle'}).text
                image = soup.find('div', {'id': 'img-canvas'}).img["src"]
                price = soup.find(
                    'span', 'a-size-base a-color-price a-color-price').text.replace(',', '.') or soup.find('span', 'a-button-inner').find('span', 'a-color-base').text
                print(price)
                details = soup.find('div', {"id": "detailBullets_feature_div"}).find(
                    'ul', 'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list')

                det = details.find_all('li')
                data = {}
                data['title'] = title
                data['image_url'] = image
                data['price'] = price
                details = {}
                for d in det:
                    span = d.find('span', 'a-list-item')
                    key = span.find(
                        'span', 'a-text-bold').text.replace('\n', '').encode("ascii", "ignore").decode().strip()
                    value = span.find_all('span')
                    details[key] = value[1].text.replace(
                        '\n', '').encode("ascii", "ignore").decode().strip()
                data['details'] = details

                sql = "INSERT INTO  amazon_product (title, image, price, details) VALUES (%s, %s, %s, %s)"
                val = (title, image, price, "details")
                mycursor.execute(sql, val)

                list.append(data)
                print(list)

            except:
                print('not availabe')

        else:
            print("URL Not Available")

    print(list)
    with open("sample.json", "w") as outfile:
        json.dump(list, outfile)

    mydb.commit()


url_generator()
