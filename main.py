import math
from conf import betway_cookies, betway_json_data, betway_headers, pointsbet_headers
from requests import get, post
import time


start_time = time.time()

# Game Id's
kambi_game_id = 1019734392
sportsbook_game_id = 1679428.3
betonline_props_game_id = 184251
betway_game_id = 13502524
pointsbet_game_id = 531591

# URL's
url_kambi = f"https://eu-offering-api.kambicdn.com/offering/v2018/pivusinrl-law/betoffer/event/{kambi_game_id}.json?lang=en_US&market=US&client_id=2&channel_id=7&ncid=1712278601199&includeParticipants=true"
url_betway = "https://sportsapi.betway.com/api/Events/v2/GetEventDetails"
url_sportsbook = f"https://canada.sportsbook.fanduel.com/cache/psevent/UK/1/false/{sportsbook_game_id}.json"
url_betonline_props_shots = f"https://bv2.digitalsportstech.com/api/dfm/marketsBySs?sb=betonline&gameId={betonline_props_game_id}&statistic=Shots"
url_betonline_props_shots_on_target = f"https://bv2.digitalsportstech.com/api/dfm/marketsBySs?sb=betonline&gameId={betonline_props_game_id}&statistic=Shots%2520on%2520Goal"
url_points_bet_shots = f"https://api.on.pointsbet.com/api/mes/v3/events/{pointsbet_game_id}"


# KAMBI
def kambi(url):
    kambi_shots_on_target_odds = list()
    kambi_shots_odds = list()
    kambi_shots_on_target_odds_under = list()
    kambi_shots_odds_under = list()
    # Get the JSON with all the possible events using GET method
    data = get(url).json()['betOffers']
    # Filter the array of all the events and add to the list only the event called "Player's shots on target"
    for i in range(len(data)):

        if data[i]["criterion"]["englishLabel"] == "Player's shots on target (Settled using Opta data)":
            # Shots on target
            # Get only odds for Over event but not Under event
            over = data[i]["outcomes"][0]
            under = data[i]["outcomes"][1]  # In case we need Under values

            kambi_shots_on_target_odds.append({over["participant"]: {"goal": over["line"] / 1000, "odd": over["oddsAmerican"]}})
            kambi_shots_on_target_odds_under.append({under["participant"]: {"goal": under["line"] / 1000, "odd": under["oddsAmerican"]}})
        elif data[i]["criterion"]["englishLabel"] == "Player's shots (Settled using Opta data)":
            # Shots
            # Get only odds for Over event but not Under event
            over = data[i]["outcomes"][0]
            under = data[i]["outcomes"][1]  # In case we need Under values

            kambi_shots_odds.append({over["participant"]: { "goal": over["line"] / 1000, "odd": over["oddsAmerican"]}})
            kambi_shots_odds_under.append({under["participant"]: {"goal": under["line"] / 1000, "odd": under["oddsAmerican"]}})
    return kambi_shots_odds, kambi_shots_on_target_odds, kambi_shots_odds_under, kambi_shots_on_target_odds_under


# BETWAY
def betway(url, cookies, headers, json_data):
    betway_shots_on_target_odds = list()
    betway_shots_odds = list()

    # Get the list of all possible events during the game using POST method because GET is not supported by this server
    # To get the odds for specific game the "EventId" should be changed in betway_json_data variable in conf file
    data = post(
        url,
        cookies=cookies,
        headers=headers,
        json=json_data,
    ).json()["Outcomes"]

    for event in data:
        if "Shots On Target" in event["BetName"] and len(event["BetName"]) < 50 and "Team" not in event["BetName"]:
            # Get the Shots on Target Odds
            split_name = event["BetName"].split()

            if "+" in split_name[2]:
                spliter = 2
            elif "+" in split_name[1]:
                spliter = 1
            elif "+" in split_name[3]:
                spliter = 3
            else:
                continue

            # Get the players name from the name string
            player_name = " ".join(split_name[:spliter])
            # Get the minimum number of goals the player should score from the name string and minus 0.5
            goal = int("".join(event["BetName"].split()[spliter:spliter+1])[0]) - 0.5
            # Get the odds in decimal format and covert it to American
            odd = str(math.floor((event["OddsDecimal"] - 1) * 100 if event["OddsDecimal"] >= 2 else -100 / (event["OddsDecimal"] - 1)))

            betway_shots_on_target_odds.append({player_name: {"goal": goal, "odd": odd}})

        elif event["BetName"].endswith("Shots") and len(event["BetName"]) < 30 and "Match" not in event["BetName"] and "Team" not in event["BetName"]:
            # Betway Shots
            split_name = event["BetName"].split()

            if "+" in split_name[2]:
                spliter = 2
            elif "+" in split_name[1]:
                spliter = 1
            elif "+" in split_name[3]:
                spliter = 3

            # Get the players name from the name string
            player_name = " ".join(split_name[:spliter])
            # Get the minimum number of goals the player should score from the name string and minus 0.5
            goal = int("".join(event["BetName"].split()[spliter:spliter + 1])[0]) - 0.5
            # Get the odds in decimal format and covert it to American
            odd = str(math.floor(
                (event["OddsDecimal"] - 1) * 100 if event["OddsDecimal"] >= 2 else -100 / (event["OddsDecimal"] - 1)))

            betway_shots_odds.append({player_name: { "goal": goal, "odd": odd}})
    return betway_shots_odds, betway_shots_on_target_odds


# SPORTSBOOK
def sportsbook(url):
    sportsbook_shots_on_target_odds = list()
    sportsbook_shots_odds = list()
    sportsbook_data = get(url).json()["eventmarketgroups"]
    filtered_data = list()
    for i in range(len(sportsbook_data)):
        if sportsbook_data[i]["name"] == "Shots":
            filtered_data = sportsbook_data[i]["markets"][:9]

    sportsbook_data_shots_on_target = filtered_data[:4]
    sportsbook_data_shots = filtered_data[4:]

    for event in range(len(sportsbook_data_shots_on_target)):
        for player in sportsbook_data_shots_on_target[event]["selections"]:
            # Shots on target
            # Variables to calculate odds for each event
            price_up = player["currentpriceup"]
            price_down = player["currentpricedown"]

            # Special formula for this website
            odd = int((price_up * 100) / price_down) if price_up > price_down else int((price_down * 100) / price_up * (-1))
            sportsbook_shots_on_target_odds.append({player["name"]: {"goal": event+0.5, "odd": odd}})

    for event in range(len(sportsbook_data_shots)):
        for player in sportsbook_data_shots[event]["selections"]:
            # Shots
            # Variables to calculate odds for each event
            price_up = player["currentpriceup"]
            price_down = player["currentpricedown"]

            # Special formula for this website
            odd = int((price_up * 100) / price_down) if price_up > price_down else int((price_down * 100) / price_up * (-1))

            sportsbook_shots_odds.append({player["name"]: {"goal": event + 0.5, "odd": odd}})
    return sportsbook_shots_odds, sportsbook_shots_on_target_odds


# BetOnline Props
def betonline_props(url_shots, url_shots_on_target):
    betonline_props_shots_on_target_odds = list()
    betonline_props_shots_odds = list()
    betonline_props_data_shots = get(url_shots).json()[0]["players"]
    betonline_props_data_shots_on_target = get(url_shots_on_target).json()[0]["players"]

    for player in betonline_props_data_shots_on_target:
        # Shots on target
        name = player["name"]
        for event in player["markets"]:
            odds = str(math.floor(
                (event["odds"] - 1) * 100 if event["odds"] >= 2 else -100 / (event["odds"] - 1)))
            betonline_props_shots_on_target_odds.append({name: { "goal": event["value"] - 0.5, "odd": odds}})

    for player in betonline_props_data_shots:
        # Shots
        name = player["name"]
        for event in player["markets"]:
            odds = str(math.floor(
                (event["odds"] - 1) * 100 if event["odds"] >= 2 else -100 / (event["odds"] - 1)))
            betonline_props_shots_odds.append({name: {"goal": event["value"] - 0.5, "odd": odds}})
    return betonline_props_shots_odds, betonline_props_shots_on_target_odds


# Pointsbet
def pointsbet(url, header):
    pointsbet_shots_on_target_odds = list()
    pointsbet_shots_odds = list()
    pointsbet_data = get(url, headers=header).json()["fixedOddsMarkets"]
    # print(pointsbet_data.text)

    pointsbet_shots_data = list()
    pointsbet_shots_on_target_data = list()
    counter = 0
    for i in pointsbet_data:
        if i["eventClass"] == "PLAYER TOTAL SHOTS":
            pointsbet_shots_data = i["outcomes"]
            counter += 1
        elif i["eventClass"] == "PLAYER TOTAL SHOTS ON TARGET":
            pointsbet_shots_on_target_data = i["outcomes"]
            counter += 1
        if counter == 2:
            break

    for player in pointsbet_shots_data:
        name = player["name"].split(" To ")[0]
        goal = player["points"] - 0.5
        odds = str(math.floor(
            (player["price"] - 1) * 100 if player["price"] >= 2 else -100 / (player["price"] - 1)))
        pointsbet_shots_odds.append({name: {"type": "Over", "goal": goal, "odd": odds}})

    for player in pointsbet_shots_on_target_data:
        name = player["name"].split(" To ")[0]
        goal = player["points"] - 0.5
        odds = str(math.floor(
            (player["price"] - 1) * 100 if player["price"] >= 2 else -100 / (player["price"] - 1)))
        pointsbet_shots_on_target_odds.append({name: {"type": "Over", "goal": goal, "odd": odds}})

    return pointsbet_shots_odds, pointsbet_shots_on_target_odds


def printer(odds_arr):
    for i in odds_arr:
        print(i)


kambi_shots, kambi_shots_shots_on_target, kambi_shots_under, kambi_shots_shots_on_target_under = kambi(url_kambi)
betway_shots, betway_shots_on_target = betway(url_betway, betway_cookies, betway_headers, betway_json_data)
sportsbook_shot, sportsbook_shots_on_targe = sportsbook(url_sportsbook)
betonline_props_shots, betonline_props_shots_on_target = betonline_props(url_betonline_props_shots, url_betonline_props_shots_on_target)
pointsbet_shots, pointsbet_shots_on_target = pointsbet(url_points_bet_shots, pointsbet_headers)


end_time = time.time()

print(end_time-start_time)

# Sorting by Kambi

# print("Kambi Over Shots")
# print("")
#
# printer(kambi_shots)
#
# print("Kambi Over Shots On target")
# print("")
#
# printer(kambi_shots_shots_on_target)
#
# print("Kambi Under Shots")
# print("")
#
# printer(kambi_shots_under)
#
# print("Kambi Under Shots On Target")
# print("")
#
# printer(kambi_shots_shots_on_target_under)
#
# print("BetOnline Shots On Target")
# print("")
#
# printer(betonline_props_shots_on_target)
