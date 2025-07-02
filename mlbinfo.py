from datetime import date, timedelta
import statsapi
import os 
from google import genai
from google.genai import types
import json

my_api_key = os.getenv('MLB_PRED')
genai.api_key = my_api_key

# Create an genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key,
)

print("Welcome to our MLB app! We have the following two functionalities:")
print("Information Mode: We will provide valuable information on whichever team you want")
print("Good Game Predictor: You provide us a team and we will tell you which of the next 5 games will be exciting!")
mode = input("Please input 1 for Information Mode or 2 for Good Game Predictor: ")

def next_x_games(id,x):
    s = []
    today = date.today().strftime("%Y-%m-%d")
    end = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    sched = statsapi.schedule(start_date=today, end_date=end, team=id)
    upcoming = [g for g in sched if g['status'] in ('Scheduled', 'Pre-Game')][:x]
    if not upcoming:
        print("No games in the next 30 days")
        return
    print(f"\nNext {len(upcoming)} games:\n")
    for g in upcoming:
        game_day = g['game_date']
        opponent = g['away_name'] if g['home_id'] == id else g['home_name']
        venue = g['venue_name']
        line = f"{game_day} vs {opponent}  @ {venue}"
        print(line)
    print("\n")
    for g in upcoming:
        s.append({
            "game_id"   : g['game_id'],
            "game_date" : g['game_date'],
            "home_team" : g['home_name'],
            "away_team" : g['away_name'],
            "venue"     : g['venue_name']
        })
    return s
    
        
    

    
def info_mode():
    team = input("What team do you want to know about: ")
    while True:
        teams = statsapi.lookup_team(team)
        if len(teams) == 0:
            team = input("We could not find this team, please try again: ")
        elif len(teams) > 1:
            print("The following teams fit under your current description, please specify which one by using name or id")
            for t in teams:
                print("Team name:", t['name'] , " and Team id: ", t['id'])
            team = input("Please enter either team name or id: ")
        else:
            print("The", teams[0]['teamName'], "are based out of", teams[0]['locationName'])
            last_g = statsapi.last_game(teams[0]['id'])
            boxscore = statsapi.boxscore_data(last_g, timecode=None)
            sched = statsapi.schedule(game_id=last_g)
            print("Their last game was played between the", boxscore['teamInfo']['home']['teamName'], "and the",boxscore['teamInfo']['away']['teamName'], "on", sched[0]['game_date'])
            away_runs = int(boxscore['away']['teamStats']['batting']['runs'])
            home_runs = int(boxscore['home']['teamStats']['batting']['runs'])

            if home_runs > away_runs:
                print("The", boxscore['teamInfo']['home']['teamName'], "won by", home_runs ,"runs to", away_runs)
            elif away_runs > home_runs:
                print("The", boxscore['teamInfo']['away']['teamName'], "won by", away_runs ,"runs to", home_runs)
            else:
                print("The game ended in a" , home_runs ,"to", away_runs, "tie")
            
            print("For the next 30 days this is their schedule: ")
            next_x_games(teams[0]['id'],10)

            players = statsapi.roster(teams[0]['id'])
            print("The teams roster is the follwing: ")
            print(players)
            break 


def predictor_mode():
    team = input("What team's future do you want to know about: ")
    while True:
        teams = statsapi.lookup_team(team)
        if len(teams) == 0:
            team = input("We could not find this team, please try again: ")
        elif len(teams) > 1:
            print("The following teams fit under your current description, please specify which one by using name or id")
            for t in teams:
                print("Team name:", t['name'] , "and Team id:", t['id'])
            team = input("Please enter either team name or id: ")
        else:
            t = teams[0]['id']
            s = next_x_games(t,5)
            games_json = json.dumps({"s": s}, separators=(",", ":"))
            prompt = (
                "Here are the games: \n \n" +
                "You are an MLB analyst. You will receive a JSON array called 's'.  For *each* game produce an object with:\n"
                "  • game_id            (copy)\n"
                "  • game_participants  (home team name vs away team)\n"
                "  • winner             (team name string)\n"
                "  • exciting           true/false  – mark exactly ONE game true "
                "(the matchup you expect to be the closest/highest-drama)\n"
                "Return *ONLY* a JSON array of these objects—no prose, no markdown."
                "\n"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                system_instruction= prompt
                ),
                contents = [{
                    "role": "user",
                    "parts": [
                    { "text": json.dumps({"s": s}, indent=None) }
                    ]
                }
            ]
            )
            #print(response.text)
            winning_prediction = json.loads(response.text)
            #for i in winning_prediction:
            #    print("In the game ", i['game_partipants'], "the", i['winner'], "won")
            #    if i['exciting']:
            #        print("This game was deemed the most exciting")

            for p in winning_prediction:

                away, home = map(str.strip, p["game_participants"].split("vs"))
                winner = p["winner"]
                loser  = home if winner == away else away   

                print(f"In the game {p['game_participants']}, the {winner} are predicted to beat the {loser}.")
                if p.get("exciting"):
                    print("🔥 This matchup above is expected to be the most exciting.\n")
            break


while True:
    if mode == '1':
        info_mode()
        break

    if mode == '2':
        predictor_mode()
        break
    
    if mode == '9':
        print("You have exited")
        break

    else:
        mode = input("Please enter a 1 for Information Mode, 2 for Preidction Mode, or 9 to exit")





