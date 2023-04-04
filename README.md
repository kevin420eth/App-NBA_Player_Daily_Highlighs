
# NBA players daily highlights

This application allows you to download NBA players' highlights and upload to your Youtube channel everyday automatically.

## Installation

Install the required packages below

* [ChromeDriver](https://chromedriver.chromium.org/downloads)
* [selenium](https://pypi.org/project/selenium/)
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
* [Pillow](https://pypi.org/project/Pillow/)
* [moviepy](https://pypi.org/project/moviepy/)

## Automate the task

- ### Windows

  1. Open your "Task Scheduler" app

  2. Select "Actions" in the top bar then click "Create Task"

  3. Select "Actons" in the tab and click "New"

  4. Enter the path of python executable file in the "Program/script" field

  5. Enter the path of your python script in the "Add argument" field and click "OK"

  6. Select "Trigger" in the top bar

  7. Click "New" and set the time you want the script to be executed


- ### Linux
  1. Check your enviroment variable display in your terminal with command and remember the value
  ```bash
  echo $DISPLAY
  ```

  2. In terminal, enter command to to open a editor
  ```bash
  crontab -e
  ```
  3. Add the script in the last line:
  30 8 * * * export DISPLAY=:1; python /home/kevmars/Desktop/App-NBA_Player_Daily_Highlighs/src/main.py

  4. replace the number after DISPLAY to the value you got in step 1.

  5. replace 30(minute) and 8(hour) to the time you want it to run, for instance, if you want it to run at 9:30 p.m. every day then it will be 30:21 * * *
  
* For more information of crobtab setting, check:



## Feedback

If you have any feedback, please reach out to us at kevin.eth.420@gmail.com


## Related

This documentation is made with [readme.so](https://readme.so/)

