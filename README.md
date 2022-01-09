# Wagon-Counter-Bot 
![Wagon Counter Bot Image](https://user-images.githubusercontent.com/43221618/130929520-c6de4482-474a-4030-883e-e1797cbd7531.PNG)


## Version 2.0
A simple readme file for the Wagon Count Bot

## About The Project
The 'Wagon Counter Bot' is a fully functional command-oriented program implemented using Discord.py API. The bot's purpose is to manage medial administrative level tasks in an efficent way, and to provide useful functionality to iterate through a channels message history and take relevant data to construct into a list. 


![image](https://user-images.githubusercontent.com/43221618/148702124-d02b082e-d171-43b5-87c2-6b554ce72b66.png)


## Project Inspiration
This bot was inspired by an activity in Red Dead Redemption Online (RDO), which allows you to preform wagon steals on players running deliveries. The objective of this content is to steal the player's wagon, and successfully make it to an alternative seller location. Upon successful delivery, the guild member will say type a target phrase in a designated channel to record their wagon steal. Overtime, this bots functionality grew to be able to record many other activies in RDO.

Therefore, the bot aims to give the ability to any member to look back in the message history and see how many occurrences of a target word/phrase of have been said by each user, and then return this information in a formated chart.


## Planned Features
- [ ] Auto-update channel name to update total count.
- [ ] The bot will send a message to an announcement channel, reminding members 10 minutes before 'Trade Route' starts.
- [ ] Command which returns the number of days each member has been in the guild and sorts them into a list.


## Requested Features Implemented
- [x] Each command should now return a different color.
- [x] Members list should now reflect the number of people in each role accurately.
- [x] Bot now displays Playing RDO - Wagon Stealing as a game activity.
- [x] Removed all bots in !members command.
- [x] Removed repeat members.
- [x] Updated bot command calls to reflect updates.
- [x] Fixed '!commands' clash between other bots and reset it to !command.
- [x] Making '!members' more readable by separating users into 2+ columns.
- [x] Updated the '!wagonSteals' command to search each message for 'bhwagon' and return the count.
- [X] Sends a private message to a member 24 minutes after typing 'bhwagon' in the server, to let them know their cooldown is up.
- [X] Records the amount of alive/dead bounties brought in by the player
- [X] Allows players to see how many alive / dead bounties the possee has brought by typing '!bountiesAlive', '!bountiesDead', and '!bounties'
- [X] Create a command to view the total number of wagon steals
- [X] Displays at the bottom of '!wagonSteal' the total amount of wagons stolen during the time call xx.


## Additional Administrative Features Implemented
- [x] Send embedded message announcements to #announcements
- [x] Users may send messages to the bot which will be delivered to everyone with the @admins role


## License
I retain all rights to the source code and no one may reproduce, distribute, or create derivative works from this work. 
