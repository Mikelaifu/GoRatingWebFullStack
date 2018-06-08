from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient # Database connector
import pandas as pd
app = Flask(__name__)
mongo = PyMongo(app)

conn=pymongo.MongoClient()
MongoClient('localhost', 27017)
db = conn.GOplayers_db
players = db.players

title = "GOgame with Flask"

def PullDataforComparisonChart(rank):
    lst = []
    for i in range(1 , rank+1):
        lst.append(list(players.find({"Rank": str(i)})))

    for dictt in lst[0]:
            del dictt["_id"]
    dict_list = {
        "Birthday": [lst[i][0]['Birthday'] for i in range(len(lst))],
        'Link': [lst[i][0]['Link'] for i in range(len(lst))],
        'Name': [lst[i][0]['Name'] for i in range(len(lst))],
        'Gender': [lst[i][0]['Gender'] for i in range(len(lst))],
        'Nation': [lst[i][0]['Nation'] for i in range(len(lst))],
        'Elo': [lst[i][0]['Elo'] for i in range(len(lst))],
        'Rank': [lst[i][0]['Rank'] for i in range(len(lst))],
        'Wins': [lst[i][0]['Wins'] for i in range(len(lst))],
        'Losses': [lst[i][0]['Losses'] for i in range(len(lst))],
        'Total': [lst[i][0]['Total'] for i in range(len(lst))],
        'Games': [lst[i][0]['Games'] for i in range(len(lst))]
    }
    
    Games = dict_list['Games']
    del dict_list['Games']
    
    def dictTranform(dict_list):
        df = pd.DataFrame(dict_list)
        names = list(df.columns)
        Outerlst = []
        for i in range(len(df)):
            innerList = []
            for j in range(len(names)):
                innerList.append(df.loc[i, names[j]])
            Outerlst.append(dict(zip(names, innerList)))
        return Outerlst
    
    final_list = dictTranform(dict_list)

    

    return final_list


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/player")
def playerpage():
    return render_template("player.html")

#--------------------------------------First Page----------------------------------------
@app.route('/Top10')
def Top10():

    final_list = PullDataforComparisonChart(10)
    
    return jsonify(final_list)

@app.route('/Top20')
def Top20():

    final_list = PullDataforComparisonChart(20)
    
    return jsonify(final_list)

@app.route('/Top50')
def Top50():

    final_list = PullDataforComparisonChart(50)
    
    return jsonify(final_list)
#--------------------------------------Second Page----------------------------------------
# "names" route
#   List of player names.


@app.route('/names')
def names():
    # Query metadata of the 'samples' table 
    names = players.find({}, {"_id":0,"Name":1,"Rank":1})
    name_list = [(name['Name'], name['Rank']) for name in names]
    players_list = []
    for name in name_list:
        players_list.append({"name": name[0], "rank": name[1]})
    # Return jsonified results
    return jsonify(players_list)

@app.route('/players/<rank>')
def player(rank):
    # Query metadata of the 'samples' table 
    park = players.find({"Rank":rank}, {"_id":0})
    park_info = [info for info in park]

    # Return jsonified results
    return jsonify(park_info[0])

@app.route('/recent')
def recents():
    # Query metadata of the 'samples' table 
    recent= [{
       "name" : "Recent 10 Games",
       "recent" : 10
    },{

       "name" : "Recent 20 Games",
       "recent" : 20

    },
    {
        "name" : "Recent 50 Games",
       "recent" : 50

    }]
    # Return jsonified results
    return jsonify(recent)

    




if __name__ == "__main__":
    app.run(debug=True)
    

