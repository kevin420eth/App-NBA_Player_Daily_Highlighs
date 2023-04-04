This documentation is under building...

How to set this script to auto-task

Windows:
Open your "Task Scheduler" app
Create a new task
Specify the action you want to perform in the "Action" tab
Set the time you want it to execute in "Trigger" tab

Linux:
Check your enviroment variable display in your terminal with command [echo $DISPLAY]
In terminal, do crontab -e
Add it in the last line:
30 8 * * * export DISPLAY=:1; python /home/kevmars/Desktop/App-NBA_Player_Daily_Highlighs/src/main.py

replace the number after DISPLAY to the display value of yours
replace 30(minute) and 8(hour) to the time you want it to run
for instance: if you want it to run at 9:30 p.m. every day
then it will be 30:21 * * *
For more information of crobtab setting, check:

