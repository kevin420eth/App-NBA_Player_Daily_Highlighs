import subprocess
import pychrome
import time

# subprocess.call(['C:/Users/Kevin/Desktop/App-NBA_Player_Daily_Highlighs/StartBrowser.bat'])
# time.sleep(5)
browser = pychrome.Browser(url="http://localhost:9222")
tab = browser.new_tab()

