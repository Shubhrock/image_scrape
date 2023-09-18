from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
import pymongo
logging.basicConfig(filename="scrapper.log", level = logging.INFO)
import os
import urllib

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def homepage():
    return render_template("index.html")

@app.route("/review", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            query = request.form['content'].replace(" ","")

            save_directory = "images/"

            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            response = requests.get(f"https://www.google.com/search?sca_esv=566095078&rlz=1C1CHBF_enIN1037IN1037&sxsrf=AM9HkKn5GODyPa5qvZw-vO2WtlyZfwYL_Q:1694966817186&q={query}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwiUka24g7KBAxUJed4KHVaPCmoQ0pQJegQIDRAB&biw=1536&bih=715&dpr=1.25")

            soup = BeautifulSoup(response.content, "html.parser")

            image_tags = soup.find_all("img")

            del image_tags[0]
            img_data=[]
            logging.info("raw data of image scrap")
            logging.info(image_tags)

            logging.info('get the image source URL')
            for index, image_tag in enumerate(image_tags):
                image_url = image_tag['src']
                logging.info(image_url)
                logging.info("send a request to the image URL and save the image")
                image_data = requests.get(image_url).content

                mydict = {"Index" : index, "Image" : image_data}
                img_data.append(mydict)
                with open(os.path.join(save_directory, f"{query}_{image_tags.index(image_tag)}.jpg"), "wb") as f:
                    f.write(image_data)
            pass1 = urllib.parse.quote("password@3001")
            uri = "mongodb+srv://shubh:{}@cluster0.sne4rgf.mongodb.net/?retryWrites=true&w=majority".format(pass1)
            # Create a new client and connect to the server
            client = pymongo.MongoClient(uri)
            db = client['image_scrap']
            review_col = db['image_scrap_data']
            review_col.insert_many(img_data)

            return "image loaded"

        except Exception as e:
            logging.info(e)
            return 'something is wrong'

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)



                