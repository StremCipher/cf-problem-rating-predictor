import pickle
import pandas as pd
import json
from flask import Flask ,render_template,request,jsonify
app=Flask(__name__)
@app.route("/",methods=['POST','GET'])
def loadpage():
    # return ("to return simple text")
    # return render_template('index.html') # to return html file
    model =pickle.load(open('div1_model.sav','rb')) # div11_model is compiled version of ml model
    data=pd.read_csv('contest1586.csv')  # contest1586.csv is the onput field that has to provide as input in model
    rating=model.predict(data) # geting predicted output from the model
    # print(rating)
    result = {
        'rating': list(rating) # storing rating in json format so that we can access it as api
    }
    # print(result)
    # print(result["rating"][0],result["rating"][1]) # accessing the each data of json object
    return result   # returning the json object 
app.run()

