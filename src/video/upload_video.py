import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Upload_Video:
    def upload_video(self, driver, player_name, title, game_date, assets_path, build_path):
        driver.switch_to.window(driver.window_handles[1])
        url = "https://studio.youtube.com/channel/UCr7j8DG6ZWNJf5R8LRweYBw/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D"

        driver.get(url)
        
        #Select the highlight video and upload it
        while True:
            try:
                select_file = driver.find_element(By.XPATH,"//input[@type='file']")
            except:
                driver.refresh()
                time.sleep(5)
            else:
                filepath = f'{build_path}/{game_date}/{player_name}/{player_name}.mp4'
                select_file.send_keys(filepath)
                break

        time.sleep(10)

        #Paste the title into the field
        while True:
            try:
                video_title_field = driver.find_element(By.CSS_SELECTOR,"#textbox")
            except:
                time.sleep(5)
            else:
                video_title_field.send_keys(Keys.CONTROL,"a")
                video_title_field.send_keys(Keys.DELETE)
                video_title_field.send_keys(title)
                break

        #Upload the thumbnail
        while True:
            try:
                select_thumbnail = driver.find_element(By.XPATH,"//input[@type='file']")
            except:
                print("fuck")
            else:
                filepath = f'{build_path}/{game_date}/{player_name}/thumbnail.png'
                select_thumbnail.send_keys(filepath)
                break

        #Click next step 3 times
        next_step = driver.find_element(By.CSS_SELECTOR,"#next-button > div")
        for n in range(0,3):
            while True:
                try:
                    next_step.click()
                except:
                    time.sleep(1)
                else:
                    break
        
        #Click done button
        while True:
            try:
                done_button = driver.find_element(By.CSS_SELECTOR,"#done-button > div")
                done_button.click()
            except:
                time.sleep(5)
            else:
                driver.switch_to.window(driver.window_handles[0])
                break