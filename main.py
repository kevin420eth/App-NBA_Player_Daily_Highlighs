import json, time, os, subprocess
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv

from src.data.field_goal_made import Fgm
from src.data.block_and_steal import Blk_And_Stl
from src.data.assist import Ast

from src.video.highlights_maker import Highlight_Make
from src.video.thumbnail_maker import make_thumbnail
from src.video.upload_video import Upload_Video

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    #--------------------------------------Initialize Web Driver--------------------------------------
    load_dotenv()
    CHROME_PATH = os.getenv("CHROME_PATH")
    USER_PROFILE_PATH = os.getenv("USER_PROFILE_PATH")
    PORT = os.getenv("PORT")

    # Launch Chrome in debug mode
    subprocess.Popen([CHROME_PATH, f'--remote-debugging-port={PORT}', f'--user-data-dir={USER_PROFILE_PATH}'])
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{PORT}")
    driver = webdriver.Chrome(options=chrome_options)
    
    #--------------------------------------Initialize Browser--------------------------------------


    driver.execute_script('window.open("https://youtube.com", "_blank");')

    tz = timezone('EST')
    today_date = str(datetime.now(tz)).split()[0]
    url = f"https://www.nba.com/games?date={today_date}"

    driver.switch_to.window(driver.window_handles[0])
    driver.get(url)
    driver.maximize_window()

    #--------------------------------------Accept Cookie Policy-----------------------------------------

    #Click the cookies accept button when browser first time loads a page on NBA.com
    try:
        cookie_accept_button = driver.find_element(By.ID,"onetrust-accept-btn-handler")
    except:
        pass
    else:
        cookie_accept_button.click()
        time.sleep(5)


    time.sleep(5000)
    #--------------------------------------Initialize-------------------------------------------

    fgm = Fgm()
    ast = Ast()
    blk_and_stl = Blk_And_Stl()
    hm = Highlight_Make()
    upload_video = Upload_Video()

    game_date = url.replace("https://www.nba.com/games?date=","").split("-")
    game_date_readable = f"{game_date[1]}/{game_date[2]}/{game_date[0]}"
    game_date = f"{game_date[1]}{game_date[2]}{game_date[0]}"

    basepath = os.path.dirname(__file__)
    assets_path = os.path.abspath(os.path.join(basepath, "..", "assets"))
    build_path = os.path.abspath(os.path.join(basepath, "..", "build"))

    try:
        os.mkdir(f'{build_path}')
    except:
        pass

    try:
        os.mkdir(f'{build_path}/{game_date}')
    except:
        pass

    with open(f"{build_path}/{game_date}/completed_player.txt", "a") as f:
        pass
    #---------------------------------------------Scrape Data---------------------------------------------

    game_info = []

    #Find the link of main page for each game from gamecards
    gamecard = driver.find_elements(By.CLASS_NAME,"GameCard_gcMain__q1lUW")


    #Find link, gameid and match info for each match then add them in to game_info list
    for _ in gamecard:
        game_page_link = _.find_element(By.TAG_NAME,"a").get_attribute("href")
        match_info = game_page_link.replace("https://www.nba.com/game/","").split("-")

        with open(f"{assets_path}/information/team_info.json","r") as f:
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
                        check_data = config.algorithm(fgm_data, reb_data, ast_data, stl_data, blk_data, pts_data)
                        if check_data:
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
                        with open(f"{build_path}/{game_date}/completed_player.txt", "r") as f:
                            completed_list = f.read()
                    except:
                        completed_list = ""

                    if each_player["player_name"] in completed_list:
                        pass
                    else:
                        os.mkdir(f"{build_path}/{game_date}/{each_player['player_name']}")
                        os.mkdir(f"{build_path}/{game_date}/{each_player['player_name']}/clips")

                        start_time = time.time()
                        if each_player["fgm_data"] > 0:
                            fgm.download(each_player["fgm_link"], each_player['player_name'], game_date, driver, build_path)
                            print("FGM clips are completed!")

                        if each_player["ast_data"] > 0:
                            ast.download(each_player["ast_link"], each_player["ast_data"], each_player['player_name'], game_date, driver, build_path)
                            print("AST clips are completed!")

                        if each_player["blk_data"] > 0:
                            blk_and_stl.download(each_player["blk_link"], each_player['player_name'], game_date, driver, build_path)
                            print("BLK clips are completed!")
                        
                        hm.highlight_maker(each_player["player_name"], game_date, assets_path, build_path)

                        make_thumbnail(
                        each_player["player_name"],
                        each_player["player_profile_link"],
                        each_player["pts_data"],
                        each_player["reb_data"],
                        each_player["ast_data"],
                        _['away_team'],
                        _['home_team'],
                        game_date,
                        game_date_readable,
                        assets_path,
                        build_path
                        )

                        yt_title = f"[NBA] {each_player['player_name']} Highlights | {_['away_team']} @ {_['home_team']} ({game_date_readable}) | NBA Regular Season"

                        upload_video.upload_video(driver, each_player["player_name"], _['away_team'], _['home_team'], yt_title, game_date, build_path)

                        end_time = time.time()

                        with open(f"{build_path}/{game_date}/{each_player['player_name']}/log.txt","a",encoding="utf-8") as f:
                            f.write("The title for Youtube 👇\n")
                            f.write(f"{yt_title}\n")
                            f.write(f'\n{each_player["pts_data"]}\n{each_player["reb_data"]}\n{each_player["ast_data"]}\n\n')
                            f.write(f"{_['away_team']} @ {_['home_team']}\n{game_date_readable}\n\n")
                            f.write(f"This video cost {int(end_time-start_time)} seconds to complete\n")

                        with open(f"{build_path}/{game_date}/completed_player.txt", "a") as f:
                            f.write(f'{each_player["player_name"]}\n')

                #Delete the game which is done out of game_info list
                game_info.remove(_)
                break

            time.sleep(15)
                
        
        if len(game_info) == 0:
            print("All tasks are done")
            break