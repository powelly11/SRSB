import os.path
from datetime import datetime, timedelta
import json

async def check_games():
    today = datetime.today().strftime('%Y-%m-%d')
    response = requests.get(f"{URL}{today}")
    if response.status_code == 200:
        data = response.json()
        for game in data['games']:
            if game['status'] == 'finished':
                game_id = game['id']
                players = game['players']
                high_scorers = []
                filename = f"{game_id}.json"
                if os.path.isfile(filename):
                    with open(filename, 'r') as f:
                        existing_players = json.load(f)
                else:
                    existing_players = []
                for player in players:
                    if float(player['score']) > 60.0 and player['id'] not in existing_players:
                        high_scorers.append(player)
                if high_scorers:
                    msg = f"The following players scored over 60.0 in game {game_id}: \n"
                    for player in high_scorers:
                        msg += f"{player['name']} - {player['score']} \n https://www.soraredata.com/player/{player['id']} \n"
                        existing_players.append(player['id'])
                    with open(filename, 'w') as f:
                        json.dump(existing_players, f)
                    channel = client.get_channel(your_channel_id_here)
                    await channel.send(msg)
