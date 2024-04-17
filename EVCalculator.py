"""
This file will proceed in the following steps:
1. converting both over and under to American odds
2. calculating both over and under 's implied probabilities
3. calculating the total probabilities by adding over and under ' s implied probabilities
4. return fair value by using: implied probabilities / total probabilities
"""
import random  # Importing the random module for generating random numbers
from tqdm import tqdm  # Importing tqdm for progress bar visualization

pbar = tqdm(total=20000)  # Initializing a progress bar with a total of 20000 iterations


def convert_to_american_odds(input_odds):
    '''
    This function is for converting our odds to American odds
    :param input_odds: The input odds to be converted
    :return: The converted American odds
    '''
    numerator = 100
    denominator = 100
    if input_odds > 0:  # Checking if the input odds are positive
        numerator = input_odds
    else:
        denominator = input_odds * -1  # If the input odds are negative, converting to positive for calculation
    return 1 + (numerator / denominator)  # Returning the American odds


def implied_probabilities(american_odds):
    '''
    This function is to calculate implied probabilities from American odds
    :param american_odds: The American odds
    :return: The implied probability
    '''
    return 1 / american_odds  # Calculating and returning the implied probability


def total_implied_probabilities(over_american_odds, under_american_odds):
    '''
    This function is for calculating total implied probabilities
    :param over_american_odds: The American odds for over
    :param under_american_odds: The American odds for under
    :return: The total implied probabilities
    '''
    return over_american_odds + under_american_odds  # Calculating and returning the total implied probabilities


def main(over, under):
    '''
    This function contains our main loop for the function
    :param over: The odds for over
    :param under: The odds for under
    :return: The calculated probability of over
    '''
    over_decimal = convert_to_american_odds(over)  # Converting over odds to American odds
    under_decimal = convert_to_american_odds(under)  # Converting under odds to American odds
    over_implied = implied_probabilities(over_decimal)  # Calculating implied probability for over
    under_implied = implied_probabilities(under_decimal)  # Calculating implied probability for under
    total_implied = total_implied_probabilities(over_implied, under_implied)  # Calculating total implied probabilities
    return over_implied / total_implied  # Returning the probability of over


#  This is a test case for the algorithm
for i in range(20000):  # Loop for 20000 iterations
    print('=====================================')  # Printing separator
    numerator = random.randint(-500, 500)  # Generating a random numerator
    denominator = random.randint(-500, 500)  # Generating a random denominator
    if denominator == 0 or numerator == 0:  # Checking if the denominator or numerator is zero
        continue  # Skipping the iteration if either is zero
    print(numerator)  # Printing the numerator
    print(denominator)  # Printing the denominator
    print(main(numerator, denominator))  # Calling the main function and printing the result
    pbar.update(1)  # Updating the progress bar
pbar.close()
