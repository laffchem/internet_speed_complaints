from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import user_name, pword, t_name
import time
import logging

options = webdriver.ChromeOptions()
options.add_argument("--headless")
service = Service(executable_path="/home/laff/Development/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

#Goes to speedtest website and runs the test to get the download / upload speed.
driver.get("https://speedtest.net")
start_button = driver.find_element(By.CSS_SELECTOR, '.start-button a')
start_button.click()
time.sleep(60)

down_speed = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
download = float(down_speed.get_attribute('innerHTML'))
up_speed = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span')
upload = float(up_speed.get_attribute('innerHTML'))

#Compares the contract minimum with current speed. If it's below, it sends out the tweet with speeds.
if download < 150:

    driver.get("https://www.twitter.com/login")

    time.sleep(5)

    t_login = driver.find_element(By.TAG_NAME, 'input')
    t_login.click()
    t_login.send_keys(user_name + Keys.ENTER)

    time.sleep(5)

    u_name = driver.find_element(By.TAG_NAME, 'input')
    u_name.click()
    u_name.send_keys(t_name + Keys.ENTER)

    time.sleep(5)

    password = driver.switch_to.active_element.send_keys(pword + Keys.ENTER)

    time.sleep(5)

    tweet = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')

    tweet.send_keys("@XFINITY" + Keys.ENTER + f"My current internet speed is Download: {download} Mbps, Upload: {upload} Mbps. I pay for 600Mbps, what gives?")
    
    send_tweet = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
    send_tweet.click()

else:
    print("Internet speeds are good!")

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', filename='internet_speeds.log', filemode='a')

#Keeps a running log on the machine so I can check it through ssh. This is more proof of concept for my raspberry pi as I doubt I'll be running this that often.

if download < 150:
    logging.info(f"Tweet Sent ---> Internet speeds are Download: {download} Mbps, Upload: {upload} Mbps.")
elif download > 150:
    logging.info(f"Tweet Not Sent ---> Internet Speeds are Download: {download} Mbps, Upload: {upload} Mbps. ")
else:
    logging.error('Runtime Error, Internet Crapped Out')