from selenium import webdriver

chrome_driver_path = '/home/kevmars/Desktop/App-NBA_Player_Daily_Highlighs/chromedriver'
driver = webdriver.Chrome(chrome_driver_path)

driver.get("https://www.google.com")