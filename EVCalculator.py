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
    player_name_list = list(over_dict.keys())
    for i in range(len(player_name_list)):
        player_name_over_dict = over_dict.get(player_name_list[i])
        over = int(player_name_over_dict.get('odd')[0])
        player_name_under_dict = under_dict.get(player_name_list[i])
        under = int(player_name_under_dict.get('odd')[0])
        player_name_final_dict = final_dict.get(player_name_list[i])
        final = player_name_final_dict.get('odd')[0]
        if over == 0 or under == 0:  # Checking if the denominator or numerator is zero
            continue  # Skipping the iteration if either is zero
        print('player name: ' + str(player_name_list[i]))
        print('over: ' + str(over))
        print('under: ' + str(under))
        fair_value, market_juice, EV_percentage = main(over, under, final)
        print("market juice: " + str(round(market_juice * 100, 1)) + '%')  # Calling the main function and printing the result
        print("Fair value: " + str(round(fair_value * 100, 1)) + '%')
        print('EV_percentage: ' + str(round(EV_percentage * 100, 1)) + '%')
        print('================================')


