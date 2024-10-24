import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0'}


def get_game_info(session, game_id, retries=3, timeout=10):
    url = f"https://boardgamegeek.com/boardgame/{game_id}"

    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            min_players = soup.find('span', {'itemprop': 'minValue'})
            max_players = soup.find('span', {'itemprop': 'maxValue'})

            if min_players and max_players:
                player_range = f"{min_players.get_text()}-{max_players.get_text()}"
            else:
                player_range = "N/A"
                print(f"Player range not found for game ID: {game_id}")

            play_time = soup.find('span', {'itemprop': 'timeRequired'})
            if not play_time:
                play_time = soup.find('span', {'itemprop': 'playingtime'})  # 다른 태그 탐색
            if not play_time:
                play_time = soup.find('span', text="Playing Time:")  # 특정 텍스트를 기준으로 탐색
                if play_time:
                    play_time = play_time.find_next('span')

            if play_time:
                play_time = play_time.get_text().strip()
            else:
                play_time = "N/A"
                print(f"Play time not found for game ID: {game_id}")

            return player_range, play_time

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for game ID: {game_id}. Retrying...")
            time.sleep(2)

    return "N/A", "N/A"


rank_file_path = 'C:/Users/kiusw/Desktop/zap/Rank.csv'
boardgames_df = pd.read_csv(rank_file_path, encoding='ISO-8859-1')

boardgames_df['players'] = ''
boardgames_df['playing_time'] = ''

output_file = 'C:/Users/kiusw/Desktop/zap/BoardGame_info.csv'

save_interval = 10  # 몇 번의 스크래핑 후 저장할 것인지 설정

for idx, row in boardgames_df.iterrows():
    game_id = row['id']
    print(f"Scraping game ID: {game_id}")

    players, playing_time = get_game_info(session, game_id)
    boardgames_df.at[idx, 'players'] = players
    boardgames_df.at[idx, 'playing_time'] = playing_time

    time.sleep(2)

    if (idx + 1) % save_interval == 0:
        boardgames_df[['id', 'name', 'rank', 'players', 'playing_time']].to_csv(output_file, index=False,
                                                                                encoding='utf-8-sig')
        print(f"Progress saved to {output_file} at row {idx + 1}")

boardgames_df[['id', 'name', 'rank', 'players', 'playing_time']].to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"Final data saved to {output_file}")
