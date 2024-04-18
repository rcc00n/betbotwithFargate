import math
from conf import betway_cookies, betway_json_data, betway_headers, pointsbet_headers, check_string_in_array
from requests import get, post
import time
import copy

start_time = time.time()

# Game Id's
kambi_game_id = 1019734392
sportsbook_game_id = 1679428.3
betonline_props_game_id = 184251
betway_game_id = 13502524
pointsbet_game_id = 531210

# URL's
url_kambi = f"https://eu-offering-api.kambicdn.com/offering/v2018/pivusinrl-law/betoffer/event/{kambi_game_id}.json?lang=en_US&market=US&client_id=2&channel_id=7&ncid=1712278601199&includeParticipants=true"
url_betway = "https://sportsapi.betway.com/api/Events/v2/GetEventDetails"
url_sportsbook = f"https://canada.sportsbook.fanduel.com/cache/psevent/UK/1/false/{sportsbook_game_id}.json"
url_betonline_props_shots = f"https://bv2.digitalsportstech.com/api/dfm/marketsBySs?sb=betonline&gameId={betonline_props_game_id}&statistic=Shots"
url_betonline_props_shots_on_target = f"https://bv2.digitalsportstech.com/api/dfm/marketsBySs?sb=betonline&gameId={betonline_props_game_id}&statistic=Shots%2520on%2520Goal"
url_points_bet_shots = f"https://api.on.pointsbet.com/api/mes/v3/events/{pointsbet_game_id}"


# KAMBI
def kambi(url):
    kambi_shots_on_target_odds = dict()
    kambi_shots_odds = dict()
    kambi_shots_on_target_odds_under = dict()
    kambi_shots_odds_under = dict()
    final_data_shots = list()
    final_data_shots_on_target = list()

    # Get the JSON with all the possible events using GET method
    data = get(url).json()['betOffers']

    # Filter the array of all the events and add to the list only the event called "Player's shots on target"
    for i in range(len(data)):
        if data[i]["criterion"]["englishLabel"] == "Player's shots on target (Settled using Opta data)":
            final_data_shots_on_target.append(data[i])
            kambi_shots_on_target_odds[data[i]["outcomes"][0]["participant"].split(",")[0]] = {"goal": list(), "odd": list()}
            kambi_shots_on_target_odds_under[data[i]["outcomes"][1]["participant"].split(",")[0]] = {"goal": list(), "odd": list()}
        elif data[i]["criterion"]["englishLabel"] == "Player's shots (Settled using Opta data)":
            final_data_shots.append(data[i])
            kambi_shots_odds[data[i]["outcomes"][0]["participant"].split(",")[0]] = {"goal": list(), "odd": list()}
            kambi_shots_odds_under[data[i]["outcomes"][1]["participant"].split(",")[0]] = {"goal": list(), "odd": list()}

    players_s = copy.deepcopy(kambi_shots_odds)
    players_sot = copy.deepcopy(kambi_shots_on_target_odds)

    for i in final_data_shots_on_target:
        over = i["outcomes"][0]
        under = i["outcomes"][1]

        kambi_shots_on_target_odds[over["participant"].split(",")[0]]["goal"].append(over["line"] / 1000)
        kambi_shots_on_target_odds[over["participant"].split(",")[0]]["odd"].append(int(over["oddsAmerican"]))

        kambi_shots_on_target_odds_under[under["participant"].split(",")[0]]["goal"].append(under["line"] / 1000)
        kambi_shots_on_target_odds_under[under["participant"].split(",")[0]]["odd"].append(int(under["oddsAmerican"]))

    for i in final_data_shots:
        over = i["outcomes"][0]
        under = i["outcomes"][1]

        kambi_shots_odds[over["participant"].split(",")[0]]["goal"].append(over["line"] / 1000)
        kambi_shots_odds[over["participant"].split(",")[0]]["odd"].append(int(over["oddsAmerican"]))

        kambi_shots_odds_under[under["participant"].split(",")[0]]["goal"].append(under["line"] / 1000)
        kambi_shots_odds_under[over["participant"].split(",")[0]]["odd"].append(int(under["oddsAmerican"]))

    return kambi_shots_odds, kambi_shots_on_target_odds, kambi_shots_odds_under, kambi_shots_on_target_odds_under, players_s, players_sot


# BETWAY
def betway(url, cookies, headers, json_data, players_s, players_sot, kambi_s, kambi_sot):
    betway_shots_odds = players_s
    betway_shots_on_target_odds = players_sot

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

            if player_name in players_sot.keys():
                # Get the minimum number of goals the player should score from the name string and minus 0.5
                goal = int("".join(event["BetName"].split()[spliter:spliter+1])[0]) - 0.5
                # Get the odds in decimal format and covert it to American
                odd = math.floor((event["OddsDecimal"] - 1) * 100 if event["OddsDecimal"] >= 2 else -100 / (event["OddsDecimal"] - 1))

                betway_shots_on_target_odds[player_name]["goal"].append(goal)
                betway_shots_on_target_odds[player_name]["odd"].append(odd)

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

            if player_name in players_s.keys():
                # Get the minimum number of goals the player should score from the name string and minus 0.5
                goal = int("".join(event["BetName"].split()[spliter:spliter + 1])[0]) - 0.5
                # Get the odds in decimal format and covert it to American
                odd = math.floor((event["OddsDecimal"] - 1) * 100 if event["OddsDecimal"] >= 2 else -100 / (
                            event["OddsDecimal"] - 1))

                betway_shots_odds[player_name]["goal"].append(goal)
                betway_shots_odds[player_name]["odd"].append(odd)

    return betway_shots_odds, betway_shots_on_target_odds


# SPORTSBOOK
def sportsbook(url, players_s, players_sot, kambi_s, kambi_sot):
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
def betonline_props(url_shots, url_shots_on_target, players_s, players_sot, kambi_s, kambi_sot):

    betonline_props_shots_on_target_odds = players_sot
    betonline_props_shots_odds = players_s
    betonline_props_data_shots = get(url_shots).json()[0]["players"]
    betonline_props_data_shots_on_target = get(url_shots_on_target).json()[0]["players"]

    for player in betonline_props_data_shots_on_target:
        # Shots on target
        name = player["name"].split()[-1]
        name_flag = check_string_in_array(players_sot.keys(), name)
        if name_flag:
            for event in player["markets"]:

                if (event["value"] - 0.5) in kambi_sot[name_flag]["goal"]:
                    odds = math.floor(
                        (event["odds"] - 1) * 100 if event["odds"] >= 2 else -100 / (event["odds"] - 1))
                    betonline_props_shots_on_target_odds[name_flag]["goal"].append(event["value"] - 0.5)
                    betonline_props_shots_on_target_odds[name_flag]["odd"].append(odds)

    for player in betonline_props_data_shots:
        # Shots
        name = player["name"].split()[-1]
        name_flag = check_string_in_array(players_s.keys(), name)
        if name_flag:
            for event in player["markets"]:
                if (event["value"] - 0.5) in kambi_s[name_flag]["goal"]:
                    odds = math.floor(
                        (event["odds"] - 1) * 100 if event["odds"] >= 2 else -100 / (event["odds"] - 1))
                    betonline_props_shots_odds[name_flag]["goal"].append(event["value"] - 0.5)
                    betonline_props_shots_odds[name_flag]["odd"].append(odds)
    return betonline_props_shots_odds, betonline_props_shots_on_target_odds


# Pointsbet
def pointsbet(url, header, players_s, players_sot, kambi_s, kambi_sot):
    pointsbet_shots_on_target_odds = list()
    pointsbet_shots_odds = list()
    pointsbet_data = get(url, headers=header).json()["fixedOddsMarkets"]

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
        odds = math.floor(
            (player["price"] - 1) * 100 if player["price"] >= 2 else -100 / (player["price"] - 1))
        pointsbet_shots_odds.append({name: {"type": "Over", "goal": goal, "odd": odds}})

    for player in pointsbet_shots_on_target_data:
        name = player["name"].split(" To ")[0]
        goal = player["points"] - 0.5
        odds = math.floor(
            (player["price"] - 1) * 100 if player["price"] >= 2 else -100 / (player["price"] - 1))
        pointsbet_shots_on_target_odds.append({name: {"type": "Over", "goal": goal, "odd": odds}})

    return pointsbet_shots_odds, pointsbet_shots_on_target_odds


kambi_shots, kambi_shots_on_target, kambi_shots_under, kambi_shots_on_target_under, players_shot, players_shot_on_target = kambi(url_kambi)
betway_shots, betway_shots_on_target = betway(url_betway, betway_cookies, betway_headers, betway_json_data, players_shot, players_shot_on_target, kambi_shots, kambi_shots_on_target,)
sportsbook_shot, sportsbook_shots_on_targe = sportsbook(url_sportsbook, players_shot, players_shot_on_target, kambi_shots, kambi_shots_on_target,)
betonline_props_shots, betonline_props_shots_on_target = betonline_props(url_betonline_props_shots, url_betonline_props_shots_on_target, players_shot, players_shot_on_target, kambi_shots, kambi_shots_on_target,)
pointsbet_shots, pointsbet_shots_on_target = pointsbet(url_points_bet_shots, pointsbet_headers, players_shot, players_shot_on_target, kambi_shots, kambi_shots_on_target,)


end_time = time.time()

print(end_time-start_time)

# Sorting by Kambi

for k, v in betonline_props_shots_on_target.items():
    print(k, v)
