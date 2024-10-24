from flask import Flask, request, render_template
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from functools import lru_cache

app = Flask(__name__)

file_path = 'C:/Users/kiusw/Desktop/zap/Rank.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

@lru_cache(maxsize=128)
def get_thumbnail(game_id):
    url = f'https://boardgamegeek.com/xmlapi2/thing?id={game_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        
        thumbnail = root.find('.//thumbnail')
        if thumbnail is not None:
            return thumbnail.text
        else:
            return "N/A"
    else:
        return "API 호출 실패"

def recommend_games(player_count, play_time):
    filtered_games = data[
        (data['minp'] <= player_count) & (data['maxp'] >= player_count) &
        (data['minpt'] <= play_time) & (data['maxpt'] >= play_time)
    ]
    
    games = []
    for _, row in filtered_games.iterrows():
        thumbnail_url = get_thumbnail(row['id'])
        games.append({
            'id': row['id'],
            'name': row['name'],
            'thumbnail': thumbnail_url
        })
    
    return games

@app.route('/', methods=['GET', 'POST'])
def index():
    games = []
    page = 1
    items_per_page = 9

    if request.method == 'POST':
        player_count = int(request.form['players'])
        play_time = int(request.form['playtime'])
        games = recommend_games(player_count, play_time)
        
    if request.args.get('page'):
        page = int(request.args.get('page'))
    
    start = (page - 1) * items_per_page
    end = start + items_per_page
    total_pages = (len(games) + items_per_page - 1) // items_per_page
    games_on_page = games[start:end]

    return render_template('index.html', games=games_on_page, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
