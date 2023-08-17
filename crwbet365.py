import datetime
import json
import os
import threading
from multiprocessing import Queue
from threading import Thread

from selenium.webdriver.support.wait import WebDriverWait

from base import driver_code
from market_data import get_main_market_data
import market_data

# def base_structue():
#     return {"time": "", "match_name": "", "market_data": []}




def updated_base_structure():
    return {"id": 0, "match": "", "merger": "", "last_update": "", "kickoff": "", "bookmaker": {}}


def market_structure():
    return {"line": "", "player": "", "outcomes": [
        {"odds": "", "outcome": ""}
    ]}


def list_sort(market_list):
    # Define the sorting order
    sorting_order = {
        "goals_1+": 0,
        "goals_2+": 1,
        "goals_3+": 2,
        "goals_4+": 3,
        "goals_5+": 4,
        "goals_6+": 5,
        "First": 6,
        "Last": 7,
        "10+": 8,
        "15+": 9,
        "20+": 10,
        "25+": 11,
        "30+": 12,
        "35+": 13,
        "40+": 14,
        "": 15,
    }
    sorted_data = sorted(market_list, key=lambda x: sorting_order[x["line"]])
    return list(sorted_data)


def export_match_data(match_name, match_data):
    # base_dict = base_structue()
    # base_dict["time"] = str(datetime.datetime.now())
    # base_dict["match_name"] = match_name
    # base_dict["market_data"] = match_data
    # if os.path.exists("game_data.json"):
    #     os.remove("game_data.json")
    top_markets_dict, final_match_data, i = {}, [], 0

    filtered_data = [item for item in match_data[0] if "Live match" not in item]

    # for i in range(1):
    #     print("asasdasdad",i)

    for parent_name, parent_data in zip(market_data.parent_list, filtered_data):
        markets = []
        i+=1
        base_dict = updated_base_structure()
        team_a, team_b = parent_name.split(" v ")
        print(team_a, "*******************************", team_b)
        if parent_name in parent_data:
            if "main_market_data" in parent_data[parent_name]:
                home_team_top_market = parent_data.get(parent_name).get("main_market_data").get(team_a)
                away_team_top_market = parent_data.get(parent_name).get("main_market_data").get(team_b)

                home_handicap_list = home_team_top_market.get("Handicap").split(" ") if home_team_top_market.get(
                    "Handicap") is not None else [0, 0]
                away_handicap_list = away_team_top_market.get("Handicap").split(" ") if away_team_top_market.get(
                    "Handicap") is not None else [0, 0]
                home_total_list = home_team_top_market.get("Total").split(" ") if home_team_top_market.get(
                    "Total") is not None else [0, 0, 0]
                away_total_list = away_team_top_market.get("Total").split(" ") if away_team_top_market.get(
                    "Total") is not None else [0, 0, 0]
                home_top_market = home_team_top_market.get("To Win") if home_team_top_market.get(
                    "To Win") is not None else 0
                away_top_market = away_team_top_market.get("To Win") if away_team_top_market.get(
                    "To Win") is not None else 0

                top_markets_dict = {
                    f"1 line {[float(home_handicap_list[0])]}": float(home_handicap_list[1]),
                    f"2 line {[float(away_handicap_list[0])]}": float(away_handicap_list[1]),
                    f"total points over {[float(home_total_list[1])]}": float(home_total_list[2]),
                    f"total points under {[float(away_total_list[1])]}": float(away_total_list[2]),
                    "regular time 1": float(home_top_market),
                    "regular time 2": float(away_top_market),
                    # "1 margin 40+": ,
                    # "2 margin 40+": 2.75,
                    # "1 margin 1-39": 4,
                    # "2 margin 1-39": 2.1,
                }

            if "multi_market_data" in parent_data[parent_name]:
                multi_scorer = parent_data.get(parent_name).get("multi_market_data")[0].get("Goalscorer")[0].get(
                    "Multi Scorer") if parent_data.get(parent_name).get("multi_market_data") != [] else None
                goal_scorer = parent_data.get(parent_name).get("multi_market_data")[0].get("Goalscorer")[1].get(
                    "Goalscorer") if parent_data.get(parent_name).get("multi_market_data") != [] else None
                disposal_home_team = parent_data.get(parent_name).get("multi_market_data")[1].get("Disposals")[
                    0].get(team_a) if parent_data.get(parent_name).get("multi_market_data") != [] else None
                disposal_away_team = parent_data.get(parent_name).get("multi_market_data")[1].get("Disposals")[
                    1].get(team_b) if parent_data.get(parent_name).get("multi_market_data") != [] else None

                if multi_scorer is not None:
                    for player in multi_scorer:
                        for player_name, player_data in player.items():
                            for key, value in player_data.items():
                                market_dict = market_structure()
                                if key == "Anytime":
                                    key = "goals_1+"
                                    over_key = "1+"
                                elif key == "2 or More":
                                    key = "goals_2+"
                                    over_key = "2+"
                                elif key == "3 or More":
                                    key = "goals_3+"
                                    over_key = "3+"
                                elif key == "4 or More":
                                    key = "goals_4+"
                                    over_key = "4+"
                                elif key == "5 or More":
                                    key = "goals_5+"
                                    over_key = "5+"
                                else:
                                    key = "goals_6+"
                                    over_key = "6+"
                                market_dict["line"] = key
                                market_dict["player"] = player_name
                                market_dict["outcomes"][0]["odds"] = value
                                market_dict["outcomes"][0][
                                    "outcome"] = f"{player_name} - ({key}) - over [{over_key}]"
                                markets.append(market_dict)
                else:
                    market_dict = market_structure()
                    market_dict["line"] = ""
                    market_dict["player"] = ""
                    market_dict["outcomes"][0]["odds"] = 0
                    market_dict["outcomes"][0]["outcome"] = ""
                    markets.append(market_dict)

                if goal_scorer is not None:
                    for player in goal_scorer:
                        for player_name, player_data in player.items():
                            for key, value in player_data.items():
                                market_dict = market_structure()
                                if key == "Anytime":
                                    key = "goals_1+"
                                    over_key = "1+"
                                elif key == "2 or More":
                                    key = "goals_2+"
                                    over_key = "2+"
                                elif key == "3 or More":
                                    key = "goals_3+"
                                    over_key = "3+"
                                elif key == "4 or More":
                                    key = "goals_4+"
                                    over_key = "4+"
                                elif key == "5 or More":
                                    key = "goals_5+"
                                    over_key = "5+"
                                else:
                                    key = "goals_6+"
                                    over_key = "6+"
                                market_dict["line"] = key
                                market_dict["player"] = player_name
                                market_dict["outcomes"][0]["odds"] = value
                                market_dict["outcomes"][0][
                                    "outcome"] = f"{player_name} - ({key}) - over [{over_key}]"
                                markets.append(market_dict)
                else:
                    market_dict = market_structure()
                    market_dict["line"] = ""
                    market_dict["player"] = ""
                    market_dict["outcomes"][0]["odds"] = 0
                    market_dict["outcomes"][0]["outcome"] = ""
                    markets.append(market_dict)

                if disposal_home_team is not None:
                    for player in disposal_home_team:
                        for player_name, player_data in player.items():
                            for key, value in player_data.items():
                                market_dict = market_structure()
                                market_dict["line"] = key
                                market_dict["player"] = player_name
                                market_dict["outcomes"][0]["odds"] = value
                                market_dict["outcomes"][0][
                                    "outcome"] = f"{player_name} - (disposals_{key}) - over [{key}]"
                                markets.append(market_dict)
                else:
                    market_dict = market_structure()
                    market_dict["line"] = ""
                    market_dict["player"] = ""
                    market_dict["outcomes"][0]["odds"] = 0
                    market_dict["outcomes"][0]["outcome"] = ""
                    markets.append(market_dict)

                if disposal_away_team is not None:
                    for player in disposal_away_team:
                        for player_name, player_data in player.items():
                            for key, value in player_data.items():
                                market_dict = market_structure()
                                market_dict["line"] = key
                                market_dict["player"] = player_name
                                market_dict["outcomes"][0]["odds"] = value
                                market_dict["outcomes"][0][
                                    "outcome"] = f"{player_name} - (disposals_{key}) - over [{key}]"
                                markets.append(market_dict)
                else:
                    market_dict = market_structure()
                    market_dict["line"] = ""
                    market_dict["player"] = ""
                    market_dict["outcomes"][0]["odds"] = 0
                    market_dict["outcomes"][0]["outcome"] = ""
                    markets.append(market_dict)

        markets_sorted_list = list_sort(markets)

        base_dict["id"] = i
        base_dict["match"] = parent_name
        base_dict["merger"] = f"{parent_name} | Bet365"
        base_dict["last_update"] = str(datetime.datetime.now())
        base_dict["markets"] = {
            "markets": markets_sorted_list,
            "top_markets": top_markets_dict
        }

        final_match_data.append(base_dict)

    with open("game_data.json", "w", encoding="utf-8") as file:
        json.dump(final_match_data, file, indent=4)


# Exception flag
exception_flag = threading.Event()


def run_driver(driver_num, queue):
    try:

        driver = driver_code(driver_num)  # You can use any Selenium WebDriver here
        # Add your automation code for the driver here

        # if driver:
        result = {"result_value": []}
        if driver_num == 0:
            result["result_value"] = get_main_market_data(driver, True)
        else:
            result["result_value"] = get_main_market_data(driver, False)

        driver.quit()

        queue.put(result)
        # else:
        #     driver.quit()# Put the result in the queue

    except Exception as e:
        # Set the exception flag and propagate the exception
        print(e)
        exception_flag.set()


# threads = []
result_queue = Queue()  # Create a queue to store the results

# for i in range(num_drivers):
#     t = Thread(target=run_driver, args=(i, result_queue))
#     threads.append(t)
#     t.start()

run_driver(1, result_queue)

results = []
match_name = ""
match_data = []

while not result_queue.empty():
    result = result_queue.get()
    match_name = result.get("result_value")[0]
    match_data.append(result.get("result_value")[1])
    results.append(result)

export_match_data(match_name, match_data)
