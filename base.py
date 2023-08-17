import time, os

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def remove_loader(driver):
    driver.execute_script("document.querySelector('.bl-Preloader').remove();")


def driver_code(driver_num):
    print("in driver")
    Capabilities = DesiredCapabilities.CHROME
    Capabilities["pageLoadStrategy"] = "normal"
    options = ChromeOptions()

    useragentarray = [
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.76 Mobile Safari/537.36"
    ]

    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument(f"--user-data-dir=./profile{driver_num}")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("disable-infobars")
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        "./chromedriver",
        options=options,
        desired_capabilities=Capabilities,
    )
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride", {"userAgent": useragentarray[0]}
    )

    options.add_argument("--disable-popup-blocking")
    #     driver.execute_script(
    #         """setTimeout(() => window.location.href="https://www.bet365.com.au", 100)"""
    #     )
    driver.get("https://www.bet365.com.au")

    driver.set_window_size(390, 844)

    # try:
    #     selector=driver.find_element(By.ID, 'msg_ln_1')
    #     return None
    # except :

    time.sleep(5)
    remove_loader(driver)
    return driver


    # if  not driver.find_element(By.ID,'msg_ln_1'):
    #
    #     driver.save_screenshot("/home/ubuntu/Scraping_Bet365/scree.png")
    #     time.sleep(5)
    #     remove_loader(driver)
    #     return driver
    # return None



def selector_finder(driver, selector_type, selector, flag=False):
    selector = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((selector_type, selector))
    )
    if flag:
        TOTAL_COUNT = len(selector)
        return selector, TOTAL_COUNT
    return selector


def open_new_tab(driver, url):

    driver.execute_script(

        f"""window.open('{url}', "_blank");"""
    )
    # else:
    #     driver.execute_script(
    #         f"""window.open('https://www.bet365.com.au/#/AC/B36/C20856562/D48/E1/F36/', "_blank");"""
    #     )

    time.sleep(10)
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])


def click_on_match_data(driver, selector, i=0):
    selector[i].click()


def based_on_selector_click(selector):
    selector.click()


def remove_cookies(driver):
    driver.find_element(By.CLASS_NAME, "ccm-CookieConsentPopup_Accept").click()


def match_selector(driver):
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,".crm-RibbonItemLeague_Afl",).click()

    # Open a new tab
    time.sleep(3)
    open_new_tab(driver, driver.current_url)


def get_match_counter(driver):
    time.sleep(2)
    return selector_finder(
                   driver,
                   By.CSS_SELECTOR,
                   ".src-ParticipantFixtureDetailsHigher_LhsContainerInner",
                   True,
               )


# ".src-ParticipantFixtureDetailsHigher_LhsContainerInner:not(:has(.pi-ScoreVariantSingleParticipant5))",
