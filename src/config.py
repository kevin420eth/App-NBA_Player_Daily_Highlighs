chrome_browser_path = "/usr/bin/google-chrome"

chrome_driver_path = "/home/kevmars/Desktop/App-NBA_Player_Daily_Highlighs/chromedriver"

user_profile_path = '/home/kevmars/.config/google-chrome/Profile_NBA'

youtube_uplaod_page = 'https://studio.youtube.com/channel/UCr7j8DG6ZWNJf5R8LRweYBw/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D'

def algorithm(fgm, reb, ast ,stl, blk, pts):
    if pts + reb + ast > 35:
        return True
    else:
        return False
    