import time
from datetime import datetime
from field_goal_made import Fgm
from block_and_steal import Blk_And_Stl
from assist import Ast
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


fgm = Fgm()
ast = Ast()
blk_and_stl = Blk_And_Stl()


s=Service("D:/Kevin/Programming/chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.maximize_window()

#-------------------------------------------Start-------------------------------------------

url = input("Please Enter URL:\n")
driver.get(url)

#-------------------------------------------Accept Cookie Privacy----------------------------------

#Click the cookies accept button when browser first time loads a page on NBA.com
try:
    cookie_accept_button = driver.find_element(By.ID,"onetrust-accept-btn-handler")
except:
    pass
else:
    cookie_accept_button.click()
    time.sleep(5)

#-------------------------------------------Set Game Date-------------------------------------------

game_info = driver.find_elements(By.CLASS_NAME, "GameSummary_sumHeading__OrQPg")[1]
date = game_info.find_elements(By.CLASS_NAME, "InfoCard_column__et46d")[1].text

date = str(datetime.strptime(date, "%B %d, %Y")).split(" ")[0].split("-")
date = f"{date[1]}/{date[2]}/{date[0]}"

#-------------------------------------------Scrape Data-------------------------------------------

url = f"{url}/box-score"
driver.get(url)

stat_table = driver.find_elements(By.CLASS_NAME,"StatsTableBody_tbody__uvj_P")
player_stat = {}

for _ in stat_table:
    each_row = _.find_elements(By.TAG_NAME,"tr")
    for _ in each_row:
        try:
            palyer_name = _.find_element(By.CLASS_NAME,"GameBoxscoreTablePlayer_gbpNameFull__cf_sn").text.lower()
            all_data = _.find_elements(By.CLASS_NAME,"GameBoxscoreTable_stat__jWIuU")
            fgm_data = int(all_data[1].text) #Data of field goal made
            reb_data = int(all_data[12].text) #Data of rebound
            ast_data = int(all_data[13].text) #Data of assist
            blk_data = int(all_data[15].text) #Data of block
            pts_data = int(all_data[18].text) #Data of Point

            #Find the link of field goal made video page
            if fgm_data > 0:
                fgm_link = all_data[1].find_element(By.TAG_NAME,"a").get_attribute("href")
            else:
                fgm_link = ""

            #Find the link of assist video page
            if ast_data > 0:
                ast_link = all_data[13].find_element(By.TAG_NAME,"a").get_attribute("href")
            else:
                ast_link = ""

            #Find the link of block video page
            if blk_data > 0:
                blk_link = all_data[15].find_element(By.TAG_NAME,"a").get_attribute("href")
            else:
                blk_link = ""
        except:
            pass
        else:
            #Add video page links of each player's field goal made, assist and block to player_stat dictionary
            player_stat[palyer_name] = {
                "fgm_link":fgm_link,
                "ast_link":ast_link,
                "blk_link":blk_link,
                "PTS":pts_data,
                "REB":reb_data,
                "AST":ast_data
                }

#-------------------------------------------Video Download-------------------------------------------

while True:
    while True:
        try:
            #Find the fgm_link, ast_link and blk_link of the target player
            taget_player = input("Enter player's name\n").lower()
            target_player_fgm_link = player_stat[taget_player]["fgm_link"]
            target_player_ast_link = player_stat[taget_player]["ast_link"]
            target_player_blk_link = player_stat[taget_player]["blk_link"]
            target_player_ast_data = player_stat[taget_player]["AST"]
        except KeyError:
            print("\nWrong Name! Please try again!\n")
        else:            
            break
    
    #If player's field goal made is not 0 then start downloading all videos on the page
    if target_player_fgm_link != "" :
        fgm.download(target_player_fgm_link,taget_player, driver)
        print("FGM clips are completed!")

    #If player's assist is not 0 then start downloading all videos on the page
    if target_player_ast_link != "" :
        ast.download(target_player_ast_link, target_player_ast_data, taget_player, driver)
        print("AST clips are completed!")

    #If player's block is not 0 then start downloading all videos on the page
    if target_player_blk_link != "" :
        blk_and_stl.download(target_player_blk_link,taget_player, driver)
        print("BLK clips are completed!")

    #Generate a title for the video on Youtube
    yt_title = fgm.generate_title(date)
    with open(f"C:/Users/Kevin/Desktop/{fgm.player_name}/log.txt","a",encoding="utf-8") as f:
        f.write("The new title for Youtube 👇\n")
        f.write(f"{yt_title}\n")
        f.write(f"\n{player_stat[taget_player]['PTS']}\n{player_stat[taget_player]['REB']}\n{player_stat[taget_player]['AST']}\n\n")
        f.write(f"{fgm.away_team} @ {fgm.home_team}\n{date}\n")
    
    #Back to the box page
    print("\nTask is completed!\n")
    driver.get(url)

    #Ask user to continue or not
    exit_or_not = input("Would you like to continue (Y/N)? ").lower()

    if exit_or_not == "n":
        print("\nGoodbye!\n")
        break
