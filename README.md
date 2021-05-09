# IPL T20 ball-by-ball simulator

This is an in-depth IPL ball by ball simulator that uses past data of each player in the IPL to predict outcomes on each ball based on various factors.

This is still in the pre-release phase so there are a lot of bugs.

## How to download it
(I would recommend cloning the code since it is more up to date, several bug fixes are not delivered to the exe download until about a week later)

Go to this link - http://bit.ly/2Ss1fwL (You can also use the official GitHub pre-release, I just use this link to track the number of downloads) and run the installer. (note that you will not get updates if you download this)
(DONT FORGET TO CREATE A FOLDER CALLED "scores" inside the game folder after installation)

1. Once you have downloaded the "Aducj1910_IPL_Sim" exe file click on it.
2. Click on "more info" and "run anyway" on the Windows Defender popup
3. open the "expo" folder created
4. create an empty folder inside the expo folder called "scores"
5. If you get the error that "Windows can't access the device, file" check out this video for the solution --> https://youtu.be/tGLKjq_p0Rs
6. Read the license & readme
7. run the doipl.bat or custom.bat, your match scorecards will be saved in the scores folder 

### How to run it
There will be three .bat files - 
1. custom.bat
2. IPL.bat
3. IPL_remaining.bat

In the first one, you can play any two IPL teams by inputting their initials (eg. DC, CSK, PBKS, etc.).
In the second, you just open it and simulates and entire IPL season, all the scorecards are saved in the /scores folder along with the batStats.txt and bowlStats.txt files.
In the third, you can simulate the remainder of the IPL 2021 season that has been suspended for now.

### Bugs
1. There are no no-balls or byes
2. Sometimes batsman who bowl very rarely bowl their full 4 overs
3. Due to these bugs and some more, I have not made this the final release and decided to make it public due to many requests

# Planned Features
Automatic squad selection
More dynamic run rate adjustment during chases
Captaincy
Custom tournaments
Other leagues like BBL, PSL

# Eventual Goal
This simulator has been created to eventually be part of a cricket IPL team manager game. A game where you can create your own IPL team or manage an existing one, do auctions, set fields during games, change bowling lineups, train players, hire coaches, etc. I am hoping this will also become an open-source project so do keep checking for any updates.
