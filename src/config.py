chrome_browser_path = "/usr/bin/google-chrome"

chrome_driver_path = "/home/kevmars/Desktop/App-NBA_Player_Daily_Highlighs/chromedriver"

user_profile_path = '/home/kevmars/.config/google-chrome/Profile_NBA'

def algorithm(fgm, reb, ast ,stl, blk, pts):
    if pts + reb + ast > 35:
        return True
    else:
        return False
    