from flask import Flask, render_template
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

db = client.mars




@app.route('/scrape')
def scrape_():
    db.mars.drop()
    mars_data_dict = scrape()

    db.mars.insert_one(mars_data_dict)

    return "hello"

@app.route('/')
def index():
    mars_data = list(db.mars.find())
    # print('================')
    # print('================')
    # print('================')
    # print(mars_data[0])

    return render_template('index.html', mars_data=mars_data[0])

