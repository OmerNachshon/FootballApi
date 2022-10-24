import pandas as pd
from flask import *
import json

app= Flask(__name__)

players=pd.read_csv("players21-22.csv",delimiter=";", encoding='latin1',index_col=False)
teams=pd.read_csv("teams21-22.csv",delimiter=";", encoding='latin1',index_col=False)
teams_lst=teams['Squad']
players_lst=players['Player']

@app.route('/',methods=['GET'])
def index_page():
    data={'Page':'Home','Message':'Welcome to Football Data API','Instructions':'add /player/?value=PLAYER_NAME for player info , replace player with team for team information'}
    json_dump=json.dumps(data)
    return json_dump

@app.route('/player/',methods=['GET'])
def request_player():   # /team/?value=TEAM_NAME
    vals = str(request.args.get('value')).lower().split('_')
    string = None
    for val in vals:
        if not string:
            string = val
        else:
            string = string + ' ' + val
    try:
        index = [i for i in range(len(players_lst)) if string == players_lst[i].lower()]
        if len(index)==0:
            index = [i for i in range(len(players_lst)) if string in players_lst[i].lower().split(' ')]
        values = players.iloc[index[0]]
        headers = players.columns
        data = {headers[i]: str(values[headers[i]]) for i in range(len(headers))}
        json_dump = json.dumps(data)
        return json_dump

    except Exception as e:
        data = {'Page': 'Error', 'value': str(e)}
        json_dump = json.dumps(data)
        return json_dump

@app.route('/team/',methods=['GET'])
def request_team(): # /team/?value=TEAM_NAME
    vals=str(request.args.get('value')).lower().split('_')
    string=None
    for val in vals:
        if not string:
            string=val
        else:
            string=string+' '+val
    try:
        index=[i for i in range(len(teams_lst)) if string==teams_lst[i].lower()]
        if len(index)==0:
            index = [i for i in range(len(teams_lst)) if string in teams_lst[i].lower().split(' ')]
        values=teams.iloc[index[0]]
        headers=teams.columns
        data={headers[i]:str(values[headers[i]]) for i in range(len(headers))}
        json_dump=json.dumps(data)
        return json_dump

    except Exception as e:
        data = {'Page': 'Error', 'value': str(e)}
        json_dump = json.dumps(data)
        return json_dump

if __name__ == '__main__':
    app.run(port=5002)