import requests, os, time
from selenium.webdriver.common.by import By

class Fgm:
    def download(self, url, player_name, game_date, driver, build_path):

        driver.get(url)
        time.sleep(3)

        #Find metadata including player's name, title and elements of each play in the section below the page
        driver.execute_script("window.scrollTo(0, 950)")
        
        while True:
            try:
                play_button = driver.find_elements(By.CLASS_NAME,"EventsTableEventType_made__g7pLy")
            except:
                driver.refresh()
                time.sleep(10)
            else:
                if len(play_button) != 0:
                    break

        while True:
            try:
                each_row = driver.find_elements(By.CLASS_NAME,"EventsTable_row__Gs8B9")
            except:
                driver.refresh()
                time.sleep(10)
            else:
                if len(each_row) != 0:
                    break

        #Find out when each play happened and make it in the list
        each_play_time =[]

        for _ in each_row:
            while True:
                try:
                    quarter = int(_.find_elements(By.TAG_NAME,"td")[9].text)
                except:
                    driver.refresh()
                    time.sleep(10)
                else:
                    break
            
            while True:
                try:
                    time_remaining = _.find_elements(By.TAG_NAME,"td")[10].text
                except:
                    driver.refresh()
                    time.sleep(10)
                else:
                    break

            minute = int(time_remaining.split(":")[0])
            second = int(time_remaining.split(":")[1])

            if quarter <= 4: #Play in regular time
                time_remaining_in_sec = 720*quarter-60*minute-second
            else: #Play in OT
                time_remaining_in_sec = 720*4+300*(quarter-4)-60*minute-second
                
            each_play_time.append(time_remaining_in_sec)

        #Find out each play's video url and collect it to the list

        while True:
            all_video_link =[]
            for _ in play_button:
                try:
                    _.click()
                except:
                    video_link = "None"
                else:
                    current_video = driver.find_element(By.ID,value="vjs_video_3_html5_api")
                    video_link = current_video.get_attribute("src")
                
                if video_link == "https://videos.nba.com/nba/static/missing.mp4":
                    video_link = ""

                all_video_link.append(video_link)
                
            if len(play_button) == len(all_video_link):
                break

#------------------------------------------Download the videos--------------------------------

        #Create a folder named as player's name in desktop
        try:
            os.mkdir(f"{build_path}/{game_date}/{player_name}")
        except:
            pass

        #Download each play of the player 
        n=0
        for _ in all_video_link:
            try:
                response = requests.get(_)
                with open(f"{build_path}/{game_date}/{player_name}/{each_play_time[n]}.mp4","wb") as f:
                    f.write(response.content)
            except Exception as e:
                with open(f"{build_path}/{game_date}/{player_name}/log.txt","a") as f:
                    f.write(f"{e}\n")
                    f.write(f"{ player_name}'s FGM video {n+1} of {len(all_video_link)} is missing")
                print(f"{n+1} of {len(all_video_link)} is missing!")
            else:              
                print(f"{n+1} of {len(all_video_link)} is completed!")
            finally:
                n+=1

        if len(all_video_link) == len(each_play_time):
            pass
        else:
            with open(f"{build_path}/{game_date}/videos_missing.txt", "a") as f:
                f.write(f"{player_name} - FGM video missing\n")
