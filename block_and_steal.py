import requests, os, time
from selenium.webdriver.common.by import By

class Blk_And_Stl:
    def download(self, url, player_name, driver):    
        driver.get(url)
        time.sleep(3)

        #Find metadata including player's name, title and elements of each play in the section below the page
        driver.execute_script("window.scrollTo(0, 800)")

        #Find the gameid
        gameid = url.split("GameID=")[1].split("&")[0]

        #Find the video link of each play and make them in a list
        all_video_link =[]

        while True:
            try:
                each_row = driver.find_elements(By.CLASS_NAME,"EventsTable_row__Gs8B9")
            except:
                pass
            else:
                if len(each_row) != 0:
                    break
                else:
                    driver.refresh()
                    time.sleep(10)
        
        while True:
            try:
                play_button = driver.find_elements(By.CLASS_NAME,"EventsTable_play__dtRDi")
            except:
                pass
            else:
                if len(play_button) != 0:
                    break
                else:
                    driver.refresh()
                    time.sleep(10)

        for _ in play_button:
            _.click()
            current_video = driver.find_element(By.ID,value="vjs_video_3_html5_api")
            video_link = current_video.get_attribute("src")
            all_video_link.append(video_link)

        #Find the key word for block and steal
        key_word = each_row[0].find_element(By.CLASS_NAME,"Crom_text__NpR1_").text.split("#@#")[1].split(" (")[0]

#----------------------------------------Find the time-----------------------------------------------
        while True:
            each_play_time = []
            x = 0
            for n in range(1,5):
                play_by_play_url=f"https://www.nba.com/game/{gameid}/play-by-play?period=Q{n}"
                driver.get(play_by_play_url)

                try:
                    each_paly = driver.find_elements(By.CLASS_NAME,"GamePlayByPlayRow_article__asoO2")
                except:
                    driver.refresh()

                for _ in each_paly:
                    content = _.find_element(By.CLASS_NAME,"GamePlayByPlayRow_desc__XLzrU").text

                    if key_word in content:
                        print("Found")
                        time_of_play = _.find_element(By.CLASS_NAME,"GamePlayByPlayRow_clockElement__LfzHV").text
                        if ":" in time_of_play:
                            min = int(time_of_play.split(":")[0])
                            sec = int(time_of_play.split(":")[1])
                            left_time = n*12*60 - (min*60+sec)
                        else:
                            sec = int(time_of_play.split(".")[0])
                            left_time = n*12*60-sec

                        each_play_time.append(left_time)
                    
                    if len(each_play_time) == len(all_video_link):
                        x = 1
                        break
                
                if x == 1:
                    break

            #Find the time for plays in OT if there's ot
            quarter_button = driver.find_elements(By.CLASS_NAME, "GamePlayByPlay_tab__BboK4")
            
            if len(quarter_button) == 5:
                pass
            elif len(each_play_time) == len(all_video_link):
                pass
            else:
                amount_of_quarter = len(quarter_button)-5
                for n in range(1,amount_of_quarter+1):
                    play_by_play_url = f"https://www.nba.com/game/{gameid}/play-by-play?period=OT{n}"
                    driver.get(play_by_play_url)

                    try:
                        each_paly = driver.find_elements(By.CLASS_NAME,"GamePlayByPlayRow_article__asoO2")
                    except:
                        driver.refresh()

                    for _ in each_paly:

                        content = _.find_element(By.CLASS_NAME,"GamePlayByPlayRow_desc__XLzrU").text

                        if key_word in content:
                            print("Found")
                            time_of_play = _.find_element(By.CLASS_NAME,"GamePlayByPlayRow_clockElement__LfzHV").text
                            
                            if ":" in time_of_play:
                                min = int(time_of_play.split(":")[0])
                                sec = int(time_of_play.split(":")[1])
                                left_time = 2880+n*300 - (min*60+sec)
                            else:
                                sec = int(time_of_play.split(".")[0])
                                left_time = 2880+n*300-sec

                            each_play_time.append(left_time)

                        if len(each_play_time) == len(all_video_link):
                            x = 1
                            break

                    if x == 1:
                        break
            
            if len(each_play_time) == len(all_video_link):
                break
            else:
                pass
#------------------------------------------Download the videos--------------------------------

        try:
            os.mkdir(f"C:/Users/Kevin/Desktop/{player_name}")
        except:
            pass

        #Download each play of the player 
        n=0
        for _ in all_video_link:
            try:
                response = requests.get(_)
                with open(f"C:/Users/Kevin/Desktop/{player_name}/{each_play_time[n]}.mp4","wb") as f:
                    f.write(response.content)
            except Exception as e:
                with open(f"C:/Users/Kevin/Desktop/{player_name}/log.txt","a") as f:
                    f.write(f"{e}\n")
                    f.write(f"{n+1} of {len(all_video_link)} is missing")
            else:
                print(f"{n+1} of {len(all_video_link)} is completed!")
            finally:
                n+=1

        #Make a notice if there's video missing
        if len(all_video_link) == len(each_play_time):
            pass
        else:
            with open(f"C:/Users/Kevin/Desktop/videos_missing.txt", "a") as f:
                f.write(f"{player_name} - BLK video missing\n")
