# Wagon-Counter-Bot 
![Wagon Counter Bot Image](https://user-images.githubusercontent.com/43221618/130929520-c6de4482-474a-4030-883e-e1797cbd7531.PNG)


## Version 1.1.0
A simple readme file for the Wagon Count Bot

## About The Project
The 'Wagon Counter Bot' is a fully functional command-oriented program implemented using Discord.py API. The bot's main functionality is to search through a channel's message history and return a list of users, along with the number of occurrences of a specific phrase. The bot also has popular secondary features like: 

![command call snip](https://user-images.githubusercontent.com/43221618/130944745-fd25d690-5f3d-44df-9c8a-83c020fb2ad0.PNG)


## Project Inspiration
This bot was inspired by an activity in Red Dead Redemption Online (RDO), which allows you to do wagon steals on players running pelt deliveries. The objective of this content is to steal the player's wagon, and successfully make it to an alternative seller location. Upon successful delivery, the Black Hat member will say 'bhwagon' in a designated channel to record their wagon steal. 

Therefore, the bot aims to give the ability to any member to look back in the message history and see how many occurrences of 'bhwagon' have been said by each user. Along with adding other helpful administrative commands, and other requested features recorded below.


## Planned Features
- [ ] Displays at the bottom of '!wagonSteal' the total amount of wagons stolen during the time call xx.
- [ ] Create a command to view the total number of wagon steals.
- [ ] Auto-update channel name to update total count.
- [ ] The bot will send a message to an announcement channel, reminding members 10 minutes before 'Trade Route' starts.
- [ ] Command which returns the number of days each member has been in the guild and sorts them into a list.


## Current Fixes / Implementations
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
- [X] Records the amount of alive/dead bounties brought in by the player - New!
- [X] Allows players to see how many alive / dead bounties the possee has brought by typing '!bountiesAlive', '!bountiesDead', and '!bounties'


## License
I retain all rights to the source code and no one may reproduce, distribute, or create derivative works from this work. 

However, I would love to keep this project going as much as possible. If you have any improved implementation ideas, would like to incorporate this bot into your server, or have any questions about the functionality of this project, feel free to reach out 
