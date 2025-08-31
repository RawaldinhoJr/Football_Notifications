import requests
import json
import pytz
from datetime import datetime, timedelta
from plyer import notification
from colorama import init, Fore, Style
init(autoreset=True)


def check_matches():
    notification.notify(
        title="Script Running",
        message=f"Football checker started at {datetime.now().strftime('%H:%M')}", 
        app_name="test"
    )
    
    print(f"Checking matches at {datetime.now()}")

    # teams to be included - [tottenham westham newcastle arsenal man city man utd liverpool chelsea real madrid barcelona atletico]
    pref_teams = [
        "Tottenham Hotspur FC",
        "Manchester United FC",
        "Newcastle United FC",
        "Manchester City FC",
        "Liverpool FC",
        "Chelsea FC",
        "Arsenal FC",
        "Borussia Dortmund",
        "FC Barcelona",
        "Real Madrid CF",
        "AC Milan",
        "Napoli FC",
        "Atlético de Madrid"
    ]
    slightpref_teams=[ "Manchester City FC","Liverpool FC","Chelsea FC","Arsenal FC" ,"Tottenham Hotspur FC",
        "Manchester United FC"]

    api_token = "7745a56e6ef649f89bd2ae051679ea94"
    today = datetime.now()
    end_date = today + timedelta(days=7)
    date_from = today.strftime('%Y-%m-%d')
    date_to = end_date.strftime('%Y-%m-%d')
    
    
    url = f"https://api.football-data.org/v4/matches?dateFrom={date_from}&dateTo={date_to}"
    headers = {
        'X-Auth-Token': api_token 
    }
    
    try:
        response = requests.get(url, headers=headers)
        # the atbt here gets the info from the url and headers=headers tells the site that the data is being fetched from a valid api token in headers var
        response.raise_for_status()
        data = response.json()
        
        if 'matches' in data and data['matches']: 
            # if to check if dict contains match, and condnl to check if there is a match in the list matches
            for match in data['matches']:
                # if match['status']=="SCHEDULED": 
                home_team = match['homeTeam']['name']
                away_team = match['awayTeam']['name']

                
                if home_team in pref_teams and away_team in pref_teams :
                    date = match['utcDate']
                    utc_time = datetime.fromisoformat(date.replace("Z", "+00:00"))
                    now_utc = datetime.now(pytz.utc)
                    time_until_kickoff = utc_time - now_utc
                    six_hours = timedelta(hours=6)
                    one_hour = timedelta(hours=1)
                    
                    if six_hours > time_until_kickoff > (six_hours - timedelta(minutes=5)):
                        message = f"⚽ 6-Hour Reminder!\n\n{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
                        notification.notify(
                            title="Football Match reminder",
                            message=message,
                            app_name="football reminder"
                        )
                        print(f"Sent message reminder for 6hours before kickoff between {match['homeTeam']['name']} vs {match['awayTeam']['name']}")
                    elif one_hour > time_until_kickoff > (one_hour - timedelta(minutes=5)):
                        message = f"⚽ 1-Hour Reminder!\n\n{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
                        notification.notify(
                            title="Football Match reminder",
                            message=message,
                            app_name="football reminder"
                        )                         
                        print(f"Sent message reminder for 1hour before kickoff between {match['homeTeam']['name']} vs {match['awayTeam']['name']}") 
                    
                    local_timezone = pytz.timezone("Asia/Kolkata")
                    India_time = utc_time.astimezone(local_timezone)
                    Formatted_India_time = India_time.strftime("%A %B %d %Y at %I:%M %p")
                    print(f"{Fore.BLUE}{Style.BRIGHT}CRAZY Match: {home_team} vs {away_team} on {Formatted_India_time}")
          
                    
                elif home_team in slightpref_teams or away_team in slightpref_teams:
                    date = match['utcDate']
                    utc_time = datetime.fromisoformat(date.replace("Z", "+00:00"))
                    now_utc = datetime.now(pytz.utc)
                    time_until_kickoff = utc_time - now_utc
                    six_hours = timedelta(hours=6)
                    one_hour = timedelta(hours=1)                    
                    if six_hours > time_until_kickoff > (six_hours - timedelta(minutes=5)):
                        message = f"⚽ 6-Hour Reminder!\n\n{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
                        notification.notify(
                            title="Football Match reminder",
                            message=message,
                            app_name="football reminder"
                        )
                        print(f"Sent message reminder for 6hours before kickoff between {match['homeTeam']['name']} vs {match['awayTeam']['name']}")
                    elif one_hour > time_until_kickoff > (one_hour - timedelta(minutes=5)):
                        message = f"⚽ 1-Hour Reminder!\n\n{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
                        notification.notify(
                            title="Football Match reminder",
                            message=message,
                            app_name="football reminder"
                        )                         
                        print(f"Sent message reminder for 1hour before kickoff between {match['homeTeam']['name']} vs {match['awayTeam']['name']}") 
                    
                    local_timezone = pytz.timezone("Asia/Kolkata")
                    India_time = utc_time.astimezone(local_timezone)
                    Formatted_India_time = India_time.strftime("%A %B %d %Y at %I:%M %p")                  
                    print(f"{Fore.YELLOW}{Style.BRIGHT}Match: {home_team} vs {away_team} on {Formatted_India_time}")
        else:
            print("No normal matches either to be found for today")  
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except KeyError:
        print("failed to get match data, API issue")


if __name__ == "__main__":
    check_matches()