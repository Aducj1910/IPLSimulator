# IPL T20 ball-by-ball simulator

This is an in-depth IPL ball by ball simulator that uses past data of each player in the IPL to predict outcomes on each ball based on various factors.

This is still in the pre-release phase so there are a lot of bugs.

### Contact me
Feel free to contact me for any question related to this simulator or anything really. My Discord is Adu04#1910, and my email is adish1910@gmail.com.

# Mentions
This simulator was featured on [Wisden](https://wisden.com/stories/global-t20-leagues/indian-premier-league-2021/rcb-finally-win-the-ipl-reddit-user-writes-python-script-to-simulate-remainder-of-2021-season), [CricTracker](https://www.crictracker.com/rcb-to-win-ipl-2021-a-reddit-user-simulates-the-remaining-season-through-a-python-script/), [TimesNow](https://www.timesnownews.com/sports/cricket/ipl/article/virat-kohli-to-lift-ipl-2021-title-with-rcb-suggests-python-programmed-simulation-of-remaining-season/756937), [News18](https://www.news18.com/cricketnext/news/rcb-wins-ipl-2021-this-reddit-user-has-the-answer-3734942.html), and more!

## How to download it (Better method)

You can still use the official release to download it but it hasn't been updated in 4 months and has several huge features missing, plus it can't be updated so I do not maintain it. It is easier to clone the repository as follows - 

For Windows - 

1. Download python - https://www.python.org/downloads/
2. After download, run ```pip install tabulate```
3. Install git - https://git-scm.com/downloads (I recommend watching a tutorial if you're stuck anywhere)
4. Run ```git clone https://github.com/Aducj1910/IPLSimulator``` in the terminal
5. Go to the IPLSimulator folder and run ```python main.py``` and voila!

For Linux -

1. Run ```sudo apt install python3.8 python3-pip git```
2. Run ```git clone https://github.com/Aducj1910/IPLSimulator```
3. Inside the folder, run ```pip3 install tabulate```
4. Then run ```python3 main.py```

## How to download it (Outdated method)

(I would recommend cloning the code since it is more up to date, several bug fixes are not delivered to the exe download until about a week later)

Use the official GitHub pre-release (https://github.com/Aducj1910/IPLSimulator/releases), and choose to download **only the setup exe file**. (note that you will not get updates automatically) and run the file. (see below for detailed download instruction)

1. Once you have downloaded the "Setup_Aducj1910_IPLSim" exe file click on it.
2. Click on "more info" and "run anyway" on the Windows Defender popup
3. If you get the error that "Windows can't access the device, file" check out this video for the solution --> https://youtu.be/tGLKjq_p0Rs
4. Run the setup
5. Open the "Aducj1910_IPLSIM" folder created
7. Read the license & readme
8. Run the IPL.bat or custom.bat, your match scorecards will be saved in the scores folder 

### How to run it
There will be three .bat files - 
1. custom.bat
2. IPL.bat (if you cant find the IPL table, you can see the IPL table if you scroll up past the playoff scorecards)
3. IPL_Remaining.bat

In the first one, you can play any two IPL teams by inputting their initials (eg. DC, CSK, PBKS, etc.).
In the second, you just open it and simulates and entire IPL season, all the scorecards are saved in the /scores folder along with the batStats.txt and bowlStats.txt files.
In the third, you can simulate the remainder of the IPL 2021 season that has been suspended for now.

### Bugs
1. There are no no-balls or byes
2. Sometimes the chase is a little slower during the middle overs.

# Planned Features
1. Automatic squad selection
2. More dynamic run rate adjustment during chases
3. Captaincy
4. Custom tournaments
5. Other leagues like BBL, PSL

# Update - 2022
I've started working on a newer version of this simulator from scratch that'll accomodate user-made players and possible eventual integration with other software.
