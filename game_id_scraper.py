from requests import get, post
from conf import *
import time
import concurrent.futures
start = time.time()

# TODO get the name of the games for Betway from this link https://sportsapi.betway.com/api/Events/v2/GetEvents and replace the
# existing key of the dictionary with the name of each games
# TODO to achive this add some values to the json data of the request to this url from the CURL website


def dict_sorter(dictionary):
    return {k: dictionary[k] for k in sorted(dictionary.keys())}


def kambi_game_ids(league_urls):
    kambi_ids = dict()

    for league, url in league_urls.items():
        games = dict()
        data = get(url).json()["events"]

        for event in data:
            games[event["event"]["englishName"].replace('-', 'v')] = event["event"]["id"]

        kambi_ids[league] = dict_sorter(games)

    return kambi_ids


# for k, v in kambi_game_ids(kambi_urls).items():
#     print(k, v)


def betway_game_ids(league_urls, header, json_data, cookies):
    betway_ids = dict()
    game_ids = list()
    leagues = ["england", "germany", "italy", "spain", "france", "netherlands"]
    league_type = ["premier-league", "bundesliga", "serie-a", "la-liga", "ligue-1", "eredivisie"]
    counter = 0
    for league, url in league_urls.items():
        json_data["SubCategoryCName"] = leagues[counter]
        json_data["GroupCName"] = league_type[counter]
        counter += 1
        games = dict()

        data = post(url, cookies=cookies, headers=header, json=json_data).json()["EventSummaries"]

        for event in range(len(data)):

            games[event] = data[event]["EventId"]
            game_ids.append(data[event]["EventId"])

            if str(data[event]["StartTime"])[5:7] != str(data[0]["StartTime"])[5:7]:
                games.pop(event)
                game_ids.pop()

        betway_ids[league] = games
    json_data["ExternalIds"] = game_ids
    json_data["MarketCName"] = 'win-draw-win'
    json_data["ScoreboardRequest"] = {
        'ScoreboardType': 3,
        'IncidentRequest': {},
    }
    json_data.pop("CategoryCName")
    json_data.pop("SubCategoryCName")
    json_data.pop("GroupCName")

    events = post("https://sportsapi.betway.com/api/Events/v2/GetEvents", headers=header, json=json_data, cookies=cookies).json()["Events"]
    names = [events[x]["EventName"] for x in range(len(events))]
    # print(names)
    # counter = 0

    for league in list(betway_ids.keys()):
        games = list(betway_ids[league].keys())
        for game in games:
            # print(betway_ids)
            betway_ids[league][names[counter]] = betway_ids[league].pop(game)
            counter += 1
    return betway_ids


# for k, v in betway_game_ids(betway_url, betway_ids_header, betway_ids_json_data, betwat_ids_cookies).items():
#     print(k, v)


def pointsbet_game_ids(league_urls, header):
    pointsbet_ids = dict()

    for league, url in league_urls.items():
        games = dict()

        data = get(url, headers=header).json()["events"]

        for event in data:

            games[event["name"]] = event["key"]

        pointsbet_ids[league] = dict_sorter(games)

    return pointsbet_ids


# for k, v in pointsbet_game_ids(pointsbet_urls).items():
#     print(k, v)


def betonline_game_ids(league_urls):
    betonline_ids = dict()

    for league, url in league_urls.items():
        games = dict()

        data = get(url).json()

        for event in data:

            games[event["team1"][0]["title"] + " vs " + event["team2"][0]["title"]] = event["_id"]

        betonline_ids[league] = dict_sorter(games)

    return betonline_ids


# for k, v in betonline_game_ids(betonline_urls).items():
#     print(k, v)


def sportsbook_game_ids(league_urls):
    sportsbook_ids = dict()

    for league, url in league_urls.items():
        games = dict()

        data = get(url).json()["events"]

        for event in data:
            games[event["eventname"]] = event["idfoevent"]

        sportsbook_ids[league] = dict_sorter(games)

    return sportsbook_ids


with concurrent.futures.ThreadPoolExecutor() as executor:
    kambi_ids = executor.submit(kambi_game_ids, kambi_urls)
    betway_ids = executor.submit(betway_game_ids, betway_url, betway_ids_header, betway_ids_json_data, betway_cookies)
    betonline_ids = executor.submit(betonline_game_ids, betonline_urls)
    sportsbook_ids = executor.submit(sportsbook_game_ids, sportsbook_urls)
    pointsbet_ids = executor.submit(pointsbet_game_ids, pointsbet_urls, pointsbet_headers)

    kambi_ids = kambi_ids.result()
    betway_ids = betway_ids.result()
    betonline_ids = betonline_ids.result()
    sportsbook_ids = sportsbook_ids.result()
    pointsbet_ids = pointsbet_ids.result()

print("Kambi\n")

for k, v in kambi_ids.items():
    print(k, v)
print("==========================================================================\n")
print("Betway\n")

for k, v in betway_ids.items():
    print(k, v)
print("==========================================================================\n")
print("Pointsbet\n")

for k, v in pointsbet_ids.items():
    print(k, v)
print("==========================================================================\n")
print("Betonline\n")

for k, v in betonline_ids.items():
    print(k, v)
print("==========================================================================\n")
print("Sportsbook\n")

for k, v in sportsbook_ids.items():
    print(k, v)
print("==========================================================================\n")


end = time.time()

print(end-start)
