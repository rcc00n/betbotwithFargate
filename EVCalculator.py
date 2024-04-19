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
        # player_name_final_dict = final_dict.get(player_name_list[i])
        # final = player_name_final_dict.get('odd')[0]
        final = 264
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


kambi_over = {'Townsend': {'goal': [0.5], 'odd': ['133']}, 'Onyedinma': {'goal': [0.5], 'odd': ['170']},
              'Morris': {'goal': [0.5], 'odd': ['-152']}, 'Woodrow': {'goal': [0.5], 'odd': ['-132']},
              'Chong': {'goal': [0.5], 'odd': ['123']}, 'Berry': {'goal': [0.5], 'odd': ['138']},
              'Barkley': {'goal': [0.5], 'odd': ['-130']}, 'Clark': {'goal': [0.5], 'odd': ['175']},
              'Ghoddos': {'goal': [0.5], 'odd': ['133']}, 'Schade': {'goal': [0.5], 'odd': ['100']},
              'Onyeka': {'goal': [0.5], 'odd': ['133']}, 'Baptiste': {'goal': [0.5], 'odd': ['190']},
              'Lewis-Potter': {'goal': [0.5], 'odd': ['-110']}, 'Yarmolyuk': {'goal': [0.5], 'odd': ['210']},
              'Wissa': {'goal': [0.5], 'odd': ['-177']}, 'Trevitt': {'goal': [0.5], 'odd': ['112']},
              'Toney': {'goal': [0.5, 1.5], 'odd': ['-360', '138']}, 'Reguilón': {'goal': [0.5], 'odd': ['205']},
              'Mbeumo': {'goal': [1.5, 0.5], 'odd': ['220', '-210']}, 'Damsgaard': {'goal': [0.5], 'odd': ['150']},
              'Maupay': {'goal': [0.5], 'odd': ['-148']}}

kambi_under = {'Townsend': {'goal': [0.5], 'odd': ['-200']}, 'Onyedinma': {'goal': [0.5], 'odd': ['-278']},
               'Morris': {'goal': [0.5], 'odd': ['105']}, 'Woodrow': {'goal': [0.5], 'odd': ['-107']},
               'Chong': {'goal': [0.5], 'odd': ['-186']}, 'Berry': {'goal': [0.5], 'odd': ['-210']},
               'Barkley': {'goal': [0.5], 'odd': ['-109']}, 'Clark': {'goal': [0.5], 'odd': ['-286']},
               'Ghoddos': {'goal': [0.5], 'odd': ['-200']}, 'Schade': {'goal': [0.5], 'odd': ['-143']},
               'Onyeka': {'goal': [0.5], 'odd': ['-200']}, 'Baptiste': {'goal': [0.5], 'odd': ['-315']},
               'Lewis-Potter': {'goal': [0.5], 'odd': ['-129']}, 'Yarmolyuk': {'goal': [0.5], 'odd': ['-360']},
               'Wissa': {'goal': [0.5], 'odd': ['118']}, 'Trevitt': {'goal': [0.5], 'odd': ['-165']},
               'Toney': {'goal': [0.5, 1.5], 'odd': ['210', '-210']}, 'Reguilón': {'goal': [0.5], 'odd': ['-345']},
               'Mbeumo': {'goal': [1.5, 0.5], 'odd': ['-385', '138']}, 'Damsgaard': {'goal': [0.5], 'odd': ['-235']},
               'Maupay': {'goal': [0.5], 'odd': ['102']}}


kambi_final = {'Townsend': {'goal': [1.5, 3.5, 4.5, 0.5, 2.5], 'odd': ['800', '7900', '20000', '125', '2900']},
               'Onyedinma': {'goal': [0.5, 4.5, 1.5, 3.5, 2.5], 'odd': ['125', '20000', '800', '7900', '2900']},
               'Morris': {'goal': [1.5, 0.5, 3.5, 4.5, 2.5], 'odd': ['100', '-400', '1000', '2400', '400']},
               'Woodrow': {'goal': [], 'odd': []}, 'Chong': {'goal': [3.5, 2.5, 0.5, 1.5, 4.5], 'odd': ['7400', '2400', '100', '700', '17500']},
               'Berry': {'goal': [1.5, 4.5, 2.5, 0.5, 3.5], 'odd': ['800', '20000', '2900', '125', '7900']},
               'Barkley': {'goal': [4.5, 0.5, 1.5, 2.5, 3.5], 'odd': ['10000', '-143', '400', '1300', '3400']},
               'Clark': {'goal': [1.5, 0.5, 4.5, 2.5, 3.5], 'odd': ['800', '125', '20000', '2900', '7900']},
               'Ghoddos': {'goal': [], 'odd': []}, 'Schade': {'goal': [], 'odd': []},
               'Onyeka': {'goal': [4.5, 2.5, 3.5, 0.5, 1.5], 'odd': ['20000', '2900', '7900', '125', '800']},
               'Baptiste': {'goal': [], 'odd': []}, 'Lewis-Potter': {'goal': [1.5, 0.5, 4.5, 3.5, 2.5], 'odd': ['500', '-125', '12500', '3900', '1600']},
               'Yarmolyuk': {'goal': [], 'odd': []}, 'Wissa': {'goal': [4.5, 0.5, 2.5, 3.5, 1.5], 'odd': ['6400', '-200', '900', '2400', '250']},
               'Trevitt': {'goal': [], 'odd': []}, 'Toney': {'goal': [2.5, 0.5, 1.5, 3.5, 4.5], 'odd': ['600', '-286', '150', '1400', '4400']},
               'Reguilón': {'goal': [], 'odd': []}, 'Mbeumo': {'goal': [1.5, 3.5, 2.5, 0.5, 4.5], 'odd': ['100', '1000', '400', '-400', '2400']},
               'Damsgaard': {'goal': [0.5, 2.5, 3.5, 1.5, 4.5], 'odd': ['125', '2900', '7900', '800', '20000']},
               'Maupay': {'goal': [4.5, 3.5, 2.5, 1.5, 0.5], 'odd': ['2900', '1100', '500', '125', '-334']}}


calculation_per_website(kambi_over, kambi_under, kambi_final)
