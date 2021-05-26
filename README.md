# IPL T20 ball-by-ball simulator

This is an in-depth IPL ball by ball simulator that uses past data of each player in the IPL to predict outcomes on each ball based on various factors.

This is still in the pre-release phase so there are a lot of bugs.

## How to download it
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
2. Sometimes batsman who bowl very rarely bowl their full 4 overs
3. Due to these bugs and some more, I have not made this the final release and decided to make it public due to many requests

# Mentions
This simulator was featured on [Wisden](https://wisden.com/stories/global-t20-leagues/indian-premier-league-2021/rcb-finally-win-the-ipl-reddit-user-writes-python-script-to-simulate-remainder-of-2021-season), [CricTracker](https://www.crictracker.com/rcb-to-win-ipl-2021-a-reddit-user-simulates-the-remaining-season-through-a-python-script/), [TimesNow](https://www.timesnownews.com/sports/cricket/ipl/article/virat-kohli-to-lift-ipl-2021-title-with-rcb-suggests-python-programmed-simulation-of-remaining-season/756937), [News18](https://www.news18.com/cricketnext/news/rcb-wins-ipl-2021-this-reddit-user-has-the-answer-3734942.html), and more!

# Planned Features
Automatic squad selection
More dynamic run rate adjustment during chases
Captaincy
Custom tournaments
Other leagues like BBL, PSL

# Eventual Goal
This simulator has been created to eventually be part of a cricket IPL team manager game. A game where you can create your own IPL team or manage an existing one, do auctions, set fields during games, change bowling lineups, train players, hire coaches, etc. I am hoping this will also become an open-source project so do keep checking for any updates.


