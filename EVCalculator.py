import self as self
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import StaleElementReferenceException


# Create a element wrapper class to prevent when page refresh the elements can't be found issue(which will occur
# because the crazyCodeNinja website does so each time hit calculate button)
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
        '''
        This function will take an function input and try to execute it for 3 times
        :param func:
        :return:
        '''
        tries = 3
        for _ in range(tries):
            try:
                return func()
            except StaleElementReferenceException:
                self.locate_element()  # Re-locate the element
        raise StaleElementReferenceException("Failed after {} retries".format(tries))

    def click(self):
        '''
        Wrapper method for driver.click
        :return:
        '''
        self.retry_operation(lambda: self.element.click())

    def send_keys(self, keys):
        '''
        Wrapper method for driver.send_key
        :param keys:
        :return:
        '''
        self.retry_operation(lambda: self.element.send_keys(keys))

class EVCalculator:
    '''
    This class is the actual ev calculator, we will run the headless mode of webdriver
    '''
    def __init__(self, url, Leg_odds: list, final_odds: list, NUM_OF_CALCULATION):
        '''
        The EVCalculator will take 4 parameters, the first one is the url addresses of the EV website we use. The second
        one is a list of numerators and third one is its corresponding denominator list, finally the last one will be
        the number of calculations that will take place.
        :param url:
        :param Leg_odds:
        :param final_odds:
        :param NUM_OF_CALCULATION:
        '''
        self.url = url
        self.Leg_odds = Leg_odds
        self.final_odds = final_odds
        self.NUM_OF_CALC = NUM_OF_CALCULATION
        # Instantiate Edge WebDriver
        edge_options = Options()
        edge_options.add_argument('--headless')
        # headless mode to hide the browser
        self.driver = webdriver.Edge(options=edge_options)
        self.driver.get(self.url)
        self.leg_odds_wrapper = ElementWrapper(self.driver, By.NAME, 'TextBoxLegOdds')
        self.final_odds_wrapper = ElementWrapper(self.driver, By.NAME, 'TextBoxFinalOdds')
        self.calculate_button_wrapper = ElementWrapper(self.driver, By.ID, 'ButtonCalculate')
        self.otpt_wrapper = ElementWrapper(self.driver, By.ID, 'LabelOutput')



    def calculate(self):
        '''

        :return:
        '''
        #pbar = tqdm(total=100)
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
            print(otpt_list[10] + otpt_list[11])
            #pbar.update(1)

        #pbar.close()
        self.driver.close()


# This part is a sample for testing purpose
leg_odds = ['-110/-110', '-110/-109', '-110/-108', '-110/-107', '-110/-106', '-110/-105']
final_odds = ['+264', '+263', '+262', '+261', '+260', '+259']
url = 'http://crazyninjamike.com/public/sportsbooks/sportsbook_devigger.aspx'
EVCalculator = EVCalculator(url, leg_odds, final_odds, 6)
EVCalculator.calculate()
