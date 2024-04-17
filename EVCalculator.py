'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import StaleElementReferenceException



# Create a element wrapper class to prevent when page refresh the elements can't be found issue(which will occur
# because the crazyCodeNinja website does so each time hit calculate button)
from time import sleep


class ElementWrapper:
    def __init__(self, driver, locator_strategy, locator_string):
        self.driver = driver
        self.locator_strategy = locator_strategy
        self.locator_string = locator_string
        self.element = None

    def locate_element(self):
        try:
            self.element = self.driver.find_element(self.locator_strategy, self.locator_string)
        except NoSuchElementException:
            print("Element not found")

    def retry_operation(self, func):

        tries = 3
        for _ in range(tries):
            try:
                return func()
            except StaleElementReferenceException:
                self.locate_element()  # Re-locate the element
        raise StaleElementReferenceException("Failed after {} retries".format(tries))

    def click(self):

        self.retry_operation(lambda: self.element.click())

    def send_keys(self, keys):
        self.retry_operation(lambda: self.element.send_keys(keys))



class EVCalculator:

    def __init__(self, url, Leg_odds: list, final_odds: list, NUM_OF_CALCULATION):
        self.url = url
        self.Leg_odds = Leg_odds
        self.final_odds = final_odds
        self.NUM_OF_CALC = NUM_OF_CALCULATION
        # Instantiate Edge WebDriver
        edge_options = Options()
        edge_options.add_argument('--headless')
        # headless mode to hide the browser
        self.driver = webdriver.Edge(options=edge_options)
        #self.driver = webdriver.Edge()
        self.driver.get(self.url)
        self.leg_odds_wrapper = ElementWrapper(self.driver, By.NAME, 'TextBoxLegOdds')
        self.final_odds_wrapper = ElementWrapper(self.driver, By.NAME, 'TextBoxFinalOdds')
        self.calculate_button_wrapper = ElementWrapper(self.driver, By.ID, 'ButtonCalculate')
        self.otpt_wrapper = ElementWrapper(self.driver, By.ID, 'LabelOutput')
        self.result = []



    def calculate(self):
        pbar = tqdm(total=100)
        for i in range(self.NUM_OF_CALC):
            # Locate and interact with the elements using the wrappers
            self.leg_odds_wrapper.locate_element()
            # Delete the elements that exists in the input box
            self.leg_odds_wrapper.send_keys(Keys.CONTROL + "a")
            self.leg_odds_wrapper.send_keys(Keys.DELETE)
            # input the new elements
            self.leg_odds_wrapper.send_keys(self.Leg_odds[i])

            # Same logic apply from previous paragraph
            self.final_odds_wrapper.locate_element()
            self.final_odds_wrapper.send_keys(Keys.CONTROL + "a")
            self.final_odds_wrapper.send_keys(Keys.DELETE)
            self.final_odds_wrapper.send_keys(self.final_odds[i])

            self.calculate_button_wrapper.locate_element()
            self.calculate_button_wrapper.click()

            # Retrieve and print the output
            self.otpt_wrapper.locate_element()
            otpt_list = self.otpt_wrapper.element.text.split(' ')
            self.result.append(otpt_list[10])
            pbar.update(1)

        pbar.close()
        self.driver.close()


# This part is a sample for testing purpose
legOdds = ['-110/-110', '-110/-111', '-110/-112', '-110/-113', '-110/-114', '-110/-115', '-110/-116', '-110/-117', '-110/-118', '-110/-119', '-110/-120', '-110/-121', '-110/-122', '-110/-123', '-110/-124', '-110/-125', '-110/-126', '-110/-127', '-110/-128', '-110/-129', '-110/-130', '-110/-131', '-110/-132', '-110/-133', '-110/-134', '-110/-135', '-110/-136', '-110/-137', '-110/-138', '-110/-139', '-110/-140', '-110/-141', '-110/-142', '-110/-143', '-110/-144', '-110/-145', '-110/-146', '-110/-147', '-110/-148', '-110/-149', '-110/-150', '-110/-151', '-110/-152', '-110/-153', '-110/-154', '-110/-155', '-110/-156', '-110/-157', '-110/-158', '-110/-159', '-110/-160', '-110/-161', '-110/-162', '-110/-163', '-110/-164', '-110/-165', '-110/-166', '-110/-167', '-110/-168', '-110/-169', '-110/-170', '-110/-171', '-110/-172', '-110/-173', '-110/-174', '-110/-175', '-110/-176', '-110/-177', '-110/-178', '-110/-179', '-110/-180', '-110/-181', '-110/-182', '-110/-183', '-110/-184', '-110/-185', '-110/-186', '-110/-187', '-110/-188', '-110/-189', '-110/-190', '-110/-191', '-110/-192', '-110/-193', '-110/-194', '-110/-195', '-110/-196', '-110/-197', '-110/-198', '-110/-199', '-110/-200', '-110/-201', '-110/-202', '-110/-203', '-110/-204', '-110/-205', '-110/-206', '-110/-207', '-110/-208', '-110/-209']
final_odds = ['+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264', '+264']
url = 'http://crazyninjamike.com/public/sportsbooks/sportsbook_devigger.aspx'
EVCalculator = EVCalculator(url, legOdds, final_odds, len(legOdds))
EVCalculator.calculate()
print(EVCalculator.result)

'''
'''
This file will proceed in the following steps:
1. converting both over and under to American odds
2. calculating both over and under 's implied probabilities
3. calculating the total probabilities by adding over and under ' s implied probabilities
4. return 
'''
import random
from tqdm import tqdm

pbar = tqdm(total = 20000)

def convert_to_american_odds(input_odds):
    '''
    This function is for converting our odds to American odds
    :param input_odds:
    :return:
    '''
    numerator = 100
    denominator = 100
    if input_odds > 0:
        numerator = input_odds
    else:
        denominator = input_odds * -1
    return  1 + (numerator/denominator)


def implied_probabilities(american_odds):
    '''
    This function is to calculating implied probabilities
    :param american_odds:
    :return:
    '''
    return 1/american_odds


def total_implied_probabilities(over_american_odds, under_american_odds):
    '''
    This function is for calculating implied probabilities
    :param over_american_odds:
    :param under_american_odds:
    :return:
    '''
    return over_american_odds + under_american_odds

def main(over, under):
    '''
    This function contains our main loop for the function
    :param over:
    :param under:
    :return:
    '''
    over_decimal = convert_to_american_odds(over)
    under_decimal = convert_to_american_odds(under)
    over_implied = implied_probabilities(over_decimal)
    under_implied = implied_probabilities(under_decimal)
    total_implied = total_implied_probabilities(over_implied, under_implied)
    return (over_implied/total_implied)
    # print(under_implied/total_implied)

#  This is a test case for the algorithm
for i in range(20000):
    print('=====================================')
    numerator = random.randint(-500, 500)
    denominator = random.randint(-500, 500)
    if denominator == 0 or numerator == 0:
        continue
    print(numerator)
    print(denominator)
    print(main(numerator, denominator))
    pbar.update(1)

