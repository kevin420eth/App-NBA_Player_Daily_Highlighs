import json, time, os
from datetime import datetime
from data.field_goal_made import Fgm
from data.block_and_steal import Blk_And_Stl
from data.assist import Ast
from video.highlights_maker import Highlight_Make
from video.thumbnail_maker import make_thumbnail
from video.upload_video import Upload_Video
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#--------------------------------------Initialize Selenium--------------------------------------

s = Service("D:/Kevin/Programming/chromedriver.exe")
chrome_options = Options()

chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(service=s, options=chrome_options)

url = "https://www.nba.com/games?date=2023-3-8"
driver.get(url)

driver.maximize_window()

#--------------------------------------Set Cookie Policy-----------------------------------------

#Click the cookies accept button when browser first time loads a page on NBA.com
try:
    cookie_accept_button = driver.find_element(By.ID,"onetrust-accept-btn-handler")
except:
    pass
else:
    cookie_accept_button.click()
    time.sleep(5)

#--------------------------------------Initialize-------------------------------------------

fgm = Fgm()
ast = Ast()
blk_and_stl = Blk_And_Stl()
hm = Highlight_Make()
upload_video = Upload_Video()

today_date = str(datetime.now()).split()[0].replace("-","")
game_date = url.replace("https://www.nba.com/games?date=","").split("-")
game_date = f"{game_date[1]}/{game_date[2]}/{game_date[0]}"

os.mkdir(f'./{game_date}')

with open(f"./{game_date}/completed_player-{today_date}.txt", "a") as f:
    pass
#---------------------------------------------Scrape Data---------------------------------------------

game_info = []

#Find the link of main page for each game from gamecards
gamecard = driver.find_elements(By.CLASS_NAME,"GameCard_gcMain__q1lUW")


#Find link, gameid and match info for each match then add them in to game_info list
for _ in gamecard:
    game_page_link = _.find_element(By.TAG_NAME,"a").get_attribute("href")
    match_info = game_page_link.replace("https://www.nba.com/game/","").split("-")

    with open("../assets/information/team_info.json","r") as f:
        team_dict = json.load(f)

    away_team = team_dict[match_info[0].upper()]["Name"]
    home_team = team_dict[match_info[2].upper()]["Name"]
    match_teams = f"{match_info[0]}-vs-{match_info[2]}"
    gameid = match_info[3]

    game_info.append({
        "away_team":away_team,
        "home_team":home_team,
        "match_team":match_teams,
        "gameid":gameid,
        "game_page_link":game_page_link
        })


while True:
    for _ in game_info:
        highlight_player = []
        box_page = f'{_["game_page_link"]}/box-score#box-score'

        try:
            driver.get(box_page)
            time.sleep(3)
            #Check videos are prepared or not by inspecting if FGM link in first tatal row is available or not
            link_of_total_fgm = driver.find_element(By.CLASS_NAME,"GameBoxscoreTable_statBold__8Jy3I").find_element(By.TAG_NAME,"a").get_attribute("href")
        except Exception as e:
            print(f'The videos of {_["match_team"]} are not ready yet!')
        else:
            #Collect the two tables(away team and home team) on the page
            stat_table = driver.find_elements(By.CLASS_NAME,"StatsTableBody_tbody__uvj_P")

            for n in stat_table:
                each_row = n.find_elements(By.TAG_NAME,"tr")
                each_row.remove(each_row[-1]) #Remove the total row form tha table

                #Collect each player's stat on the table
                for m in each_row:
                    player_name = m.find_element(By.CLASS_NAME,"GameBoxscoreTablePlayer_gbpNameFull__cf_sn").text
                    player_profile_link = m.find_element(By.CLASS_NAME,"GameBoxscoreTablePlayer_link___fXjS").get_attribute("href")
                    try:
                        all_data = m.find_elements(By.CLASS_NAME,"GameBoxscoreTable_stat__jWIuU")
                        fgm_data = int(all_data[1].text) #Data of field goal made
                        reb_data = int(all_data[12].text) #Data of rebound
                        ast_data = int(all_data[13].text) #Data of assist
                        stl_data = int(all_data[14].text) #Data of steal
                        blk_data = int(all_data[15].text) #Data of block
                        pts_data = int(all_data[18].text) #Data of Point
                    except IndexError:
                        pass
                    except Exception as e:
                        print(e)
                        

                    #Check if the total of PTS + REB + AST reaches 36 and start downloading process
                    if pts_data + reb_data + ast_data > 35:
                        try:
                            fgm_link = all_data[1].find_element(By.TAG_NAME,"a").get_attribute("href")
                        except Exception as e:
                            fgm_link = ""

                        try:
                            ast_link = all_data[13].find_element(By.TAG_NAME,"a").get_attribute("href")
                        except Exception as e:
                            ast_link = ""

                        try:
                            blk_link = all_data[15].find_element(By.TAG_NAME,"a").get_attribute("href")
                        except Exception as e:
                            blk_link = ""

                        highlight_player.append(
                            {
                            "player_name":player_name,
                            "player_profile_link":player_profile_link,
                            "fgm_data":fgm_data,
                            "pts_data":pts_data,
                            "reb_data":reb_data,
                            "ast_data":ast_data,
                            "blk_data":blk_data,
                            "fgm_link":fgm_link,
                            "ast_link":ast_link,
                            "blk_link":blk_link
                            }
                        )

            for each_player in highlight_player:
                try:
                    with open(f"./{game_date}/completed_player-{today_date}.txt", "r") as f:
                        completed_list = f.read()
                except:
                    completed_list = ""

                if each_player["player_name"] in completed_list:
                    pass
                else:
                    if each_player["fgm_data"] > 0:
                        fgm.download(each_player["fgm_link"], each_player['player_name'], today_date, driver)
                        print("FGM clips are completed!")

                    if each_player["ast_data"] > 0:
                        ast.download(each_player["ast_link"], each_player["ast_data"], each_player['player_name'], today_date, driver)
                        print("AST clips are completed!")

                    if each_player["blk_data"] > 0:
                        blk_and_stl.download(each_player["blk_link"], each_player['player_name'], today_date, driver)
                        print("BLK clips are completed!")

                    yt_title = f"[NBA] {each_player['player_name']} Highlights | {_['away_team']} @ {_['home_team']} ({game_date}) | NBA Regular Season"

                    with open(f"C:/Users/Kevin/Desktop/{each_player['player_name']}/log.txt","a",encoding="utf-8") as f:
                        f.write("The new title for Youtube 👇\n")
                        f.write(f"{yt_title}\n")
                        f.write(f'\n{each_player["pts_data"]}\n{each_player["reb_data"]}\n{each_player["ast_data"]}\n\n')
                        f.write(f"{_['away_team']} @ {_['home_team']}\n{game_date}\n")
                    
                    hm.highlight_maker(each_player["player_name"], game_date)

                    make_thumbnail(
                    each_player["player_name"],
                    each_player["player_profile_link"],
                    each_player["pts_data"],
                    each_player["reb_data"],
                    each_player["ast_data"],
                    _['away_team'],
                    _['home_team'],
                    game_date
                    )

                    upload_video.upload_video(driver,each_player["player_name"], yt_title, game_date)

                    with open(f"./{game_date}/completed_player-{today_date}.txt", "a") as f:
                        f.write(f'{each_player["player_name"]}\n')

            #Delete the game which is done out of game_info list
            game_info.remove(_)
            break

        time.sleep(15)
            
    
    if len(game_info) == 0:
        print("All tasks are done")
        break
