"""
This file will proceed in the following steps:
1. converting both over and under to American odds
2. calculating both over and under 's implied probabilities
3. calculating the total probabilities by adding over and under ' s implied probabilities
4. return fair value by using: implied probabilities / total probabilities
"""
import random  # Importing the random module for generating random numbers


def convert_to_decimal_odds(american_odds):
    if american_odds > 0:
        return 1 + american_odds / 100
    elif american_odds < 0:
        return 1 + 100 / abs(american_odds)
    else:
        raise ValueError("Odds cannot be zero")


def implied_probabilities(american_odds):
    '''
    This function is to calculate implied probabilities from American odds
    :param american_odds: The American odds
    :return: The implied probability
    '''
    return 1 / american_odds  # Calculating and returning the implied probability


def total_implied_probabilities(over_implied, under_implied):
    return over_implied + under_implied



def market_juice_calculation(total_implied_prob):
    return total_implied_prob - 1

def EV_calculation(fair_value_probabilities, final_odds_decimal):
    x = fair_value_probabilities * final_odds_decimal
    y = 1 - fair_value_probabilities
    return x - y

def main(over, under, final):
    '''
    This function contains our main loop for the function
    :param final:
    :param over: The odds for over
    :param under: The odds for under
    :return: The calculated probability of over
    '''
    over_decimal = convert_to_decimal_odds(over)  # Converting over odds to American odds
    under_decimal = convert_to_decimal_odds(under)  # Converting under odds to American odds
    final_decimal = convert_to_decimal_odds(final) - 1
    over_implied = implied_probabilities(over_decimal)  # Calculating implied probability for over
    under_implied = implied_probabilities(under_decimal)  # Calculating implied probability for under
    total_implied = total_implied_probabilities(over_implied, under_implied)  # Calculating total implied probabilities
    market_juice = market_juice_calculation(total_implied)
    fair_value = over_implied / total_implied
    EV_percentage = EV_calculation(fair_value, final_decimal)
    return fair_value, market_juice, EV_percentage  # Returning the probability of over


def calculation_per_website(over_dict: dict, under_dict: dict, final_dict: dict):
    return_value = {}  # this is the dictionary we going to return such that contain all the information
    player_name_list = list(over_dict.keys())
    for i in range(len(player_name_list)):  # obtain the value of dictionary based on the key that is players name
        player_name_over_dict = over_dict.get(player_name_list[i])
        over_list = player_name_over_dict.get('odd')
        player_name_under_dict = under_dict.get(player_name_list[i])
        under_list = player_name_under_dict.get('odd')
        player_name_final_dict = final_dict.get(player_name_list[i])
        final_list = player_name_final_dict.get('odd')
        fair_value_list = []
        market_juice_list = []
        EV_percentage_list = []
        goal = []
        goal_legOdds_finalOdds_FV_EV_MJ_dict = {}
        for over_odds, under_odds, final_odds in zip(over_list, under_list, final_list):  # obtain the
            over = int(over_odds)
            under = int(under_odds)
            final = int(final_odds)
            if over == 0 or under == 0 or final is None:  # Checking if the denominator or numerator is zero
                continue  # Skipping the iteration if either is zero
            print('player name: ' + str(player_name_list[i]))
            print('over: ' + str(over))
            print('under: ' + str(under))
            print("final_odds: " + str(final))
            fair_value, market_juice, EV_percentage = main(over, under, final)
            fair_value_list.append(fair_value)
            market_juice_list.append(market_juice)
            EV_percentage_list.append(EV_percentage)
            print("market juice: " + str(round(market_juice * 100, 1)) + '%')  # Calling the main function and printing the result
            print("Fair value: " + str(round(fair_value * 100, 1)) + '%')
            print('EV_percentage: ' + str(round(EV_percentage * 100, 1)) + '%')
            print('================================')
        temp_dict = {}
        for k in range(len(fair_value_list)):
            temp_dict[fair_value_list[k]] = k
        dict(sorted(temp_dict.items()))  # here we will sort the temp_dict in ascending orders
        greatest_fair_value_in_fair_value_list_index = temp_dict[list(temp_dict.keys())[-1]]
        if greatest_fair_value_in_fair_value_list_index > 0.5:
            goal_legOdds_finalOdds_FV_EV_MJ_dict['goal'] = over_dict[player_name_list[i]]['goal']
            goal_legOdds_finalOdds_FV_EV_MJ_dict['Leg Odds'] = str(over_list[greatest_fair_value_in_fair_value_list_index]) + str(under_list[greatest_fair_value_in_fair_value_list_index])
            goal_legOdds_finalOdds_FV_EV_MJ_dict['Final Odds'] = str(final_list[greatest_fair_value_in_fair_value_list_index])
            goal_legOdds_finalOdds_FV_EV_MJ_dict['Fair value'] = fair_value_list[greatest_fair_value_in_fair_value_list_index]
            goal_legOdds_finalOdds_FV_EV_MJ_dict['EV percentage'] = EV_percentage_list[greatest_fair_value_in_fair_value_list_index]
            goal_legOdds_finalOdds_FV_EV_MJ_dict['Market juice'] = market_juice_list[greatest_fair_value_in_fair_value_list_index]
            return_value[player_name_list[i]] = goal_legOdds_finalOdds_FV_EV_MJ_dict
    return return_value







