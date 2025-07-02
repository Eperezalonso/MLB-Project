from datetime import date, timedelta
import statsapi

print("Welcome to our MLB app! We have the following two functionalities:")
print("Information Mode: We will provide valuable information on whichever team you want")
print("Good Game Predictor: You provide us a team and we will tell you which of the next 5 games will be exciting!")
mode = input("Please input 1 for Information Mode or 2 for Good Game Predictor: ")

def next_x_games(id,x):
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
        print(f"{game_day} vs {opponent}  @ {venue}")

    
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

#def predictor_mode():

    


while True:
    if mode == '1':
        info_mode()
        break

    if mode == '2':
        predictor_mode()
    
    if mode == '9':
        print("You have exited")
        break

    else:
        mode = input("Please enter a 1 for Information Mode, 2 for Preidction Mode, or 9 to exit")





