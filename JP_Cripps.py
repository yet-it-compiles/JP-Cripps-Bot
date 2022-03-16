""" This module embeds the information sent to it within a message and sends it to the chat based on method specific
command calls. """

import asyncio
import os
import signal
import discord
import random
import CounterFunctionality
import datetime as dt
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # loads the encapsulated values from the .env file

# Declaration of Encapsulated Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Declaration Discord.py Variables
intents = discord.Intents.default()  # Turns on the connection
intents.members = True  # Ensures the member list will be updated properly
client = commands.Bot(command_prefix="!", intents=intents)  # defines the symbol used to call a command from the bot

bot_bar_color = 0x115555  # Main color for the bot response window
wagon_counter_channel = 925193742045028383
server_creation = dt.datetime(day=25, month=8, year=2021)
server_today = dt.datetime.utcnow()
start_num_days = server_today - server_creation


@client.event
async def on_ready():
    """ Sets the status of the bot when it connects to the guild """
    await client.change_presence(activity=discord.Game("RDO - Wagon Stealing"))


@client.listen()
async def on_message(message):
    """
    Listens for when a member calls 'drwagon',  refresh the counter, and after 24 minutes sends user a message

    :param message: the message sent by the user
    :type message: discord.message.Message
    :return: a DM to the user letting them know their cooldown has ended
    """
    if message.content.startswith("drwagon"):
        await wagonRefresh(message)
        await cool_down_ended(message)

    elif message.content.startswith("!"):
        await message.delete()


async def cool_down_ended(message):
    """
    Sends the author of the message a personal DM 24 minutes after they type 'drwagon' in a guild channel
    :param message: message the author sent
    :type message: discord.message.Message
    :return: a message to the author letting them know they can wagon steal again
    """
    # Variables which store pictures messages
    picture1 = discord.File("Old Cripps Looking Weathered.png")
    picture2 = discord.File("Cripps Smoking.png")

    # Defines a list which stores quotes to send to the user
    list_of_quotes = \
        [
            "Your wagon steal timer is up 🐇\nLooks like it's time for another materials run!",
            f"Hey {message.author}, looks like our materials are running low again",
            "Did you get the telegram I sent you? \nWe need to get some more materials, so lets get out there and hit "
            "another wagon.",
            "*A mailman walks up to you and hands you a letter..."
            "you open it, realizing it's from Cripps* "
            f"\n\nDear {message.author},\nI need more materials to keep our trade post running. \nBring some more "
            f"when you can.",
            f"It's huntin' time, {message.author}. Time to get on that horse!",
            "Look at Jay on that wagon list, you won't just let him top that leaderboard -that- easy, right? \nGet "
            "out there!",
            "The law should be looong gone by now, already talked to the other Dead Rabbits, we're just waiting on the "
            "call. Let's get out there again",
            "Alright folks, time to earn that money!",
            picture1,
            picture2,
        ]

    await asyncio.sleep(1440)  # sets a time for 24 minutes = 1440 seconds
    response_to_send = random.choice(list_of_quotes)  # randomizes the responses

    if response_to_send == picture1:
        await message.author.send(file=discord.File("Old Cripps Looking Weathered.png"))
    elif response_to_send == picture2:
        await message.author.send(file=discord.File("Cripps Smoking.png"))
    else:
        await message.author.send(response_to_send)


@client.event
async def on_reaction_add(reaction, user):  # reaction & user as an argument
    """
    Sends a message to a user 24 minutes later, after they react to a message

    :param reaction: '✅' - checkmark emoji/reaction
    :type reaction: discord.reaction.Reaction
    :param user: is the member who reacted to the message
    :type user: discord.member.Member
    :return: a message to the user letting them know their cool down is up
    """
    if reaction.emoji == "✅":  # See if the reaction is the same as in the code
        await asyncio.sleep(1440)  # sets a time for 24 minutes = 1440 seconds

        # Variables which store the pictures
        picture1 = discord.File("Old Cripps Looking Weathered.png")
        picture2 = discord.File("Cripps Smoking.png")

        # A list which stores the possible quotes to send to the user
        list_of_quotes = \
            [
                "Your wagon steal timer is up 🐇\nLooks like it's time for another materials run!",
                f"Hey {user}, looks like our materials are running low again",
                "Did you get the telegram I sent you? \nWe need to get some more materials, so lets get out there and "
                "hit "
                "another wagon.",
                "*A mailman walks up to you and hands you a letter..."
                "you open it, realizing it's from Cripps* "
                f"\n\nDear {user},\nI need more materials to keep our trade post running. \nBring some more "
                f"when you can.",
                f"It's huntin' time, {user}. Time to get on that horse!",
                "Look at Jay on that wagon list, you won't just let him top that leaderboard -that- easy, right? \nGet "
                "out there!",
                "Cops should be gone by now, already talked to the other Rabbits, we're just waiting on the call. "
                "Let's get out there again",
                "Did I ever tell you about the time.... wait the hell am I talkin to you for there are wagons need "
                "stealin!   And to think my Pa thought you'd be a no good trader all your life",
                "As much as I love our conversations.   Some poor bastard needs his wagon liberating from them.   "
                "Take the damn dog with you. Flea biten mongrel gives me all kinds of evils",
                "You know how Moses parted the Red Sea?   Well I can tell you like to part traders from their goods, "
                "and guess what time it is?",
                picture1,
                picture2
            ]

        response = random.choice(list_of_quotes)

        if response == picture1:
            await user.send(file=discord.File("Old Cripps Looking Weathered.png"))
        elif response == picture2:
            await user.send(file=discord.File("Cripps Smoking.png"))
        else:
            await user.send(response)


@client.command()
async def wagonSteals(ctx, days):
    """
    Defines a command which is called by typing '!wagonSteals xx' in any channel.
    The xx represents the amount of days to search back through.
    NOTE: 'Read Message History' must be turned on in Channel Permissions

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :param days: the number of days the user wants to search back in a channels message history
    :type days: str
    :return: an embedded message with a list of users and their number of occurrences of 'drwagon'
    """

    wagon_steals_data = await CounterFunctionality.RedDeadRedemptionCounter().to_client(ctx, days)
    num_of_wagon_steals = CounterFunctionality.RedDeadRedemptionCounter().calculate()

    # Defines the name of the embed message along with the site to take a member to if they click on it
    wagon_steal_message = discord.Embed(title="Wagon Steals Counter", url="https://deadrabbitsrdo.com/contest-winners/",
                                        color=bot_bar_color)

    # Assigns the author field to the member who called the bot
    wagon_steal_message.set_author(name=ctx.author.display_name, url="https://www.deadrabbitsrdo.com",
                                   icon_url=ctx.author.avatar_url)

    wagon_steal_message.set_thumbnail(url="https://media-rockstargames-com.akamaized.net/tina-uploads/posts"
                                          "/k498991k775ka8/0d8094e147c018ccd87c79294eedce3fcfcbb405.png")

    # Determines which message to print based on the users passed in 'days' argument
    if int(days) > 1:
        wagon_steal_message.add_field(name=f"Top Occurrences of 'drwagon' In The Last {days} Days",
                                      value=wagon_steals_data, inline=False)
        wagon_steal_message.set_footer(text=f"Total number of steals in the last {days} days is {num_of_wagon_steals}")
    elif int(days) == 1:
        wagon_steal_message.add_field(
            name=f"Top Occurrences of 'drwagon' In The Last Day",
            value=wagon_steals_data,
            inline=False)
        wagon_steal_message.set_footer(text=f"Total number of steals in the last {days} days is {num_of_wagon_steals}")

    await ctx.send(embed=wagon_steal_message)


@client.command()
async def bounties(ctx, days):
    """
    Defines a command which keeps track of the amount of points a player received by determined by weather or not they
    bring the bounty in dead or alive

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :param days: the number of days the user wants to search back in a channels message history
    :type days: str
    :return: an embedded message with a list of users with the amount of points they've received from their bounties
    """
    bounties_recovered_data = await CounterFunctionality.BountiesCounter().to_client(ctx, days)
    total_bounties = CounterFunctionality.BountiesCounter().calculate()

    # Defines the embed header
    bounties_recovered = discord.Embed(title="Bounty Leader Board", url="https://deadrabbitsrdo.com/contest-winners/",
                                       color=bot_bar_color)

    # Displays the person who called the command
    bounties_recovered.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    bounties_recovered.set_thumbnail(
        url="https://www.gamespot.com/a/uploads/screen_kubrick/1585/15855271/3765041-image004.png")

    # Logic to determine which embed message should send
    if int(days) > 1:
        bounties_recovered.add_field(name=f"Top Bounty Hunters in the last {days} days".title(),
                                     value=bounties_recovered_data,
                                     inline=False)
        bounties_recovered.set_footer(text=f"Total number of bounties in the last {days} days is {total_bounties}")
    elif int(days) == 1:
        bounties_recovered.add_field(name=f"Top Bounty Hunters in the last {days} day".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of bounties in the last {days} day is {total_bounties}")
    await ctx.send(embed=bounties_recovered)


@client.command()
async def bountiesDead(ctx, days):
    """
    Defines a command which is called by typing '!bountiesDead xx' in any channel.
    The xx represents the amount of days to look back through.
    NOTE: 'Read Message History' must be turned on in Channel Permissions

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :param days: the number of days the user wants to search back in a channels message history
    :type days: str
    :return: an embedded message with a list of users with the amount of points they've received from their dead bounty
    """
    bounties_recovered_data = await CounterFunctionality.DeadCounter().to_client(ctx, days)
    total_bounties = CounterFunctionality.DeadCounter().calculate()

    bounties_recovered = discord.Embed(title="Bounty Leader Board", url="https://deadrabbitsrdo.com/contest-winners/",
                                       color=bot_bar_color)

    bounties_recovered.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    bounties_recovered.set_thumbnail(url="https://www.gamespot.com/a/uploads/screen_kubrick/1585/15855271/3765041"
                                         "-image004.png")

    if int(days) > 1:
        bounties_recovered.add_field(name=f"Number of Dead Bounties Brought in the last {days} days".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of dead bounties recovered in the last {days} days is "
                                           f"{total_bounties}")
    elif int(days) == 1:
        bounties_recovered.add_field(name=f"Number of Dead Bounties Brought in the last day".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(
            text=f"Total number of dead bounties recovered in the last {days} day is {total_bounties}")
    await ctx.send(embed=bounties_recovered)


@client.command()
async def bountiesAlive(ctx, days):
    """
    Defines a command which is called by typing '!bountiesAlive xx' in any channel.
    The xx represents the amount of days to look back through.
    NOTE: 'Read Message History' must be turned on in Channel Permissions

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :param days: the number of days the user wants to search back in a channels message history
    :type days: str
    :return: an embedded message with a list of users with the amount of points they've received from their alive bounty
    """
    # returns the dictionary output list and calculates the values in the dictionary
    bounties_recovered_data = await CounterFunctionality.AliveCounter().to_client(ctx, days)
    total_bounties = CounterFunctionality.AliveCounter().calculate()

    bounties_recovered = discord.Embed(title="Bounty Leader Board", url="https://deadrabbitsrdo.com/contest-winners/",
                                       color=bot_bar_color)

    bounties_recovered.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    bounties_recovered.set_thumbnail(
        url="https://www.gamespot.com/a/uploads/screen_kubrick/1585/15855271/3765041-image004.png")

    if int(days) > 1:
        bounties_recovered.add_field(name=f"Number of Living Bounties Brought in the last {days} days".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of living bounties in the last {days} days is "
                                           f"{total_bounties}")
    elif int(days) == 1:
        bounties_recovered.add_field(name=f"Number of Living Bounties Brought in the last day".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of living bounties in the last {days} day is "
                                           f"{total_bounties}")
    await ctx.send(embed=bounties_recovered)


@client.command()
async def parley(ctx, days):
    """
    Defines a command which is called by typing '!parley xx' in any channel.
    The xx represents the amount of days to look back through.
    NOTE: 'Read Message History' must be turned on in Channel Permissions

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :param days: the number of days the user wants to search back in a channels message history
    :type days: str
    :return: an embedded message with a list of users with the amount of points they've received from their parleys
    """
    # returns the dictionary output list and calculates the values in the dictionary
    bounties_recovered_data = await CounterFunctionality.ParleyCounter().to_client(ctx, days)
    total_parleys = CounterFunctionality.ParleyCounter().calculate()

    bounties_recovered = discord.Embed(title="Parley Leader Board", url="https://deadrabbitsrdo.com/contest-winners/",
                                       color=0x1BF761)

    bounties_recovered.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    bounties_recovered.set_thumbnail(url="https://preview.redd.it/hzzvz0gi0j121.jpg?auto=webp&s"
                                         "=86411716d80ffc4516a2829ea362883ebc0ef36a")

    if int(days) > 1:
        bounties_recovered.add_field(
            name=f"Number of Parleys in the last {days} days".title(),
            value=bounties_recovered_data,
            inline=False)
        bounties_recovered.set_footer(text=f"Total number of parleys in the last {days} days is {total_parleys}")
    elif int(days) == 1:
        bounties_recovered.add_field(name=f"Number of Parleys in the last day".title(), value=bounties_recovered_data,
                                     inline=False)
        bounties_recovered.set_footer(text=f"Total number of parleys in the last {days} day is {total_parleys}")
    await ctx.send(embed=bounties_recovered)


@client.command()
async def members(ctx):
    """
    Defines the ability for a user to call '!members' in a channel and the bot will return a list of all members
    organized into two columns. The end of the message displays the total number of members in each role.

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: an embedded message displaying all the users, and how many are in each role
    """
    # Captures all members in the guild, and lists them in alphabetical order
    all_members = get_all_members()
    all_members.sort(reverse=False)

    # Splits the users into two groups for formatting
    number_of_members = len(all_members)
    first_half_of_members = int(number_of_members / 2)
    last_half_of_members = first_half_of_members + 1

    half_all_members = all_members[0:first_half_of_members]
    second_half_of_members = all_members[last_half_of_members:number_of_members]

    # defines guild role IDs
    five_pointers = ctx.guild.get_role(880159069544005702)
    dead_rabbits = ctx.guild.get_role(880156058272808981)
    short_tail = ctx.guild.get_role(880155440133062686)
    wanderer = ctx.guild.get_role(880154109041319957)

    # Declaration of embed header
    members_message = discord.Embed(title="\tCurrent Members List", url="https://deadrabbitsrdo.com", color=0x4EEDEB)

    # This shows the member who called the bot function
    members_message.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                               icon_url=ctx.author.avatar_url)

    # Shows the title of each list
    members_message.add_field(name="Member List 1 ".title(), value=str("\n".join(half_all_members)), inline=True)
    members_message.add_field(name="Member List 2".title(), value=str("\n".join(second_half_of_members)), inline=True)

    # Shows the total amount of users in each role
    members_message.add_field(name="Current member count ".title(), value=str(len(all_members)), inline=False)
    members_message.add_field(name="five_pointers count".title(), value=str(len(five_pointers.members)), inline=True)
    members_message.add_field(name="dead_rabbits count".title(), value=str(len(dead_rabbits.members)), inline=True)
    members_message.add_field(name="short tail ".title(), value=str(len(short_tail.members)), inline=True)
    members_message.add_field(name="wanderer count ".title(), value=str(len(wanderer.members)), inline=True)

    await ctx.send(embed=members_message)


@client.command()
async def guide(ctx):
    """
    Defines the ability for a user to call '!guide' in a channel and the bot will return a Survival Guide - Outlaw 101
    created by a member of the Dead Rabbits (author field)

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: a hyperlink to a website which contains the Dead Rabbits Survival Guide - Outlaw 101
    """
    guide_message = discord.Embed(title="Dead Rabbits RDO Guide - Outlaw 101",
                                  url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-"
                                      "IMlSVmjMj6g/edit#gid=837843276",
                                  description="This is the RDO Dead Rabbits Guide, which will be helpful for new and "
                                              "veteran players alike. Feel free to download a copy and use it as you "
                                              "wish!", color=bot_bar_color)

    # Displays the author of the Survival Guide
    guide_message.set_author(name="Bandit Blaggy#8895", url="https://www.twitch.tv/banditblaggy",
                             icon_url="https://cdn.discordapp.com/attachments/868317767818960978/924089703228129340/Logo.png")

    guide_message.set_thumbnail(url="https://media.discordapp.net/attachments/880157196141338705/895470756371263578"
                                    "/Guide.jpg?width=1392&height=591")

    await ctx.send(embed=guide_message)


@client.command()
async def serverRanks(ctx):
    """
    Defines the ability for a user to call '!serverRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: a complete list of all possible roles the members may earn
    """
    server_ranks_message = discord.Embed(title="Dead Rabbits RDO - Server Titles",
                                         description="A complete list of the available Server Titles",
                                         color=bot_bar_color)

    # This shows the member who called the bot function
    server_ranks_message.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                    icon_url=ctx.author.avatar_url)

    server_ranks_message.set_thumbnail(
        url="https://github.com/yet-it-compiles/Wagon-Counter-Bot/blob/main/Ranks_and_titles.jpg?raw=true")

    server_ranks_message.add_field(name="Wanderer".title(),
                                   value="The base role of the server. All members joining the server will receive this"
                                         "rank once they have acknowledged the rules. Those in this rank are in their "
                                         "probationary period to last no less than two weeks, and up to one month.",
                                   inline=False)
    server_ranks_message.add_field(name="Short Tail".title(),
                                   value="Members will progress to this rank upon a full member stepping up to take "
                                         "them on as Sponsor. These are trusted members of the crew and will now have "
                                         "the ability to request extended absences when real life intervenes and will "
                                         "not be kicked automatically for inactivity. Short Tails also get access to "
                                         "the suggestion box where they can make recommendations for the server.",
                                   inline=True)
    server_ranks_message.add_field(
        name="Dead Rabbit".title(),
        value="Members will progress to this rank upon completion of their membership checklist, concurrence of their "
              "sponsor, and completion of initiations. Dead Rabbits are full members of the crew. They are the most "
              "loyal and trusted members. Dead Rabbits have access to additional channels in the server and are "
              "eligible for Elite Ranks.", inline=False)

    server_ranks_message.set_footer(text="Membership checklist is maintained by the sponsor.")

    await ctx.send(embed=server_ranks_message)


@client.command()
async def inGameRankTitles(ctx):
    """
    Defines the ability for a user to call '!serverRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: a complete list of all possible roles the members may earn
    """
    inGameRankTitles_message = discord.Embed(title="Dead Rabbits RDO - In-Game Rank Titles",
                                             description="A complete list of the available In-Game Rank Titles",
                                             color=bot_bar_color)

    # This shows the member who called the bot function
    inGameRankTitles_message.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                        icon_url=ctx.author.avatar_url)

    inGameRankTitles_message.set_thumbnail(
        url="https://github.com/yet-it-compiles/Wagon-Counter-Bot/blob/main"
            "/Ranks_and_titles.jpg?raw=true")

    inGameRankTitles_message.add_field(name="Plug Ugly: 0-99".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="Day Breaker: 100-199".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="200-299: Night Walker".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="300-399: Black Bird".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="400-499: Slaughter Houser".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="500-599: Broadway Twister".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="600-699: Bloody Sixther".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="700-799: Autumn Diver".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="800-899: Battle Annie".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="900-999: 40 Thieves".title(), value="-", inline=False)

    inGameRankTitles_message.add_field(name="1000+: Know Nothing".title(), value="-", inline=False)

    await ctx.send(embed=inGameRankTitles_message)


@client.command()
async def monthlyEliteRanks(ctx):
    """
    Defines the ability for a user to call '!serverRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: a complete list of all possible roles the members may earn
    """
    monthlyEliteRanks_message = discord.Embed(title="Dead Rabbits RDO - Monthly Elite Ranks",
                                              url="https://deadrabbitsrdo.com/contest-winners/",
                                              description="A complete list of the available Monthly Elite Ranks",
                                              color=bot_bar_color)

    # This shows the member who called the bot function
    monthlyEliteRanks_message.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                         icon_url=ctx.author.avatar_url)

    monthlyEliteRanks_message.set_thumbnail(
        url="https://github.com/yet-it-compiles/Wagon-Counter-Bot/blob/main/Ranks_and_titles.jpg?raw=true")

    monthlyEliteRanks_message.add_field(
        name="Highwayman".title(),
        value="Awarded monthly to whoever leads the most wagon steals. Steals for this award must be performed on the "
              "server. Credit goes to whoever spotted the wagon.",
        inline=False)

    monthlyEliteRanks_message.add_field(name="Butcher".title(),
                                        value="Awarded monthly to whoever has made the most griefers quit. Quitting is "
                                              "defined as the player(s) parley, leave session, fast travel away or hide"
                                              " in a safe zone. If they hide or fast travel, you must wait for two "
                                              "minutes and verify they do not return to fight. Must be performed on "
                                              "the server. Any member of the posse may claim credit. Salty players "
                                              "after content do not count as griefers.", inline=False)
    monthlyEliteRanks_message.add_field(name="Recovery Agent".title(),
                                        value="Awarded monthly to whoever has earned the most points for player "
                                              "bounties. Alive: 1 point\n    Dead: 1/2 point\n Submissions to the "
                                              "bounty counter must be accompanied by a screenshot of the Bounty "
                                              "Complete screen. May be performed solo or in a posse. Does not have to "
                                              "be performed on the server, but is preferred.",
                                        inline=False)

    monthlyEliteRanks_message.add_field(name="Priest".title(),
                                        value="Awarded Monthly to whoever has earned the most honor as awarded by the "
                                              "membership in the #honor-counter.", inline=False)

    await ctx.send(embed=monthlyEliteRanks_message)


@client.command()
async def eliteRanks(ctx):
    """
    Defines the ability for a user to call '!serverRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild

    :param ctx: represents the context in which a command is being invoked under.
    :type ctx: discord.ext.commands.context.Context
    :return: a complete list of all possible roles the members may earn
    """
    eliteRanks_message = discord.Embed(
        title="Dead Rabbits RDO - Elite Ranks", url="https://deadrabbitsrdo.com/crew-honors/",
        description="A complete list of the available Elite Rank Titles", color=bot_bar_color)

    # This shows the member who called the bot function
    eliteRanks_message.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    eliteRanks_message.set_thumbnail(
        url="https://github.com/yet-it-compiles/Wagon-Counter-Bot/blob/main/Ranks_and_titles.jpg?raw=true")

    eliteRanks_message.add_field(name="Hell-Cat Maggie".title(),
                                 value="Love stealing wagons? This Rank goes to any member that has lead 100 wagon "
                                       "steals as tracked in the Wagon Steal Counter, and has performed at least one of"
                                       "them solo without killing anyone. The Solo No Kill steal must be witnessed by "
                                       "a full Dead Rabbit. Any steals led while a Wanderer or Short Tail will count "
                                       "towards the total.", inline=False)

    eliteRanks_message.add_field(name="Roach Guard".title(),
                                 value="These are the most feared and ruthless members of the crew when it comes to "
                                       "PvP. This Rank goes to members who have documented 50 Parleys in the counter, "
                                       "and have Defended the crew 10 times during content. (Content can be anything "
                                       "from a rival trader attempting to steal a wagon, a player bounty, or hostile "
                                       "players attacking a free roam mission.)", inline=False)

    eliteRanks_message.add_field(name="Bondsman".title(),
                                 value="Criminals flee from them. This rank goes to members who have met the following "
                                       "criteria: 50 player bounties brought in alive 50 player bounties brought in "
                                       "dead Achieved max player bounty of $100 with screenshot as proof Been turned "
                                       "in to jail with screenshot as proof", inline=False)

    eliteRanks_message.add_field(
        name="Five Pointer".title(),
        value="The Moderators of the crew. They have the authority and ability to mute, "
              "and deafen members should the rare need arise.", inline=False)

    await ctx.send(embed=eliteRanks_message)


@client.command()
async def dates(ctx):
    """
    Defines the ability for a user to call '!dates' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: a complete list of all possible roles the members may earn
    """
    progressionDates_message = discord.Embed(title="Dead Rabbits RDO - Wanderer Progression Dates",
                                             url="https://docs.google.com/spreadsheets/d/1y3GK_q1fOYUGrAZ_"
                                                 "n4cbSXGRLKwUlub0-leGYlDaEA/edit#gid=0",
                                             description="A helpful resource to view the progression dates for new "
                                                         "members", color=bot_bar_color)

    # This shows the member who called the bot function
    progressionDates_message.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                                        icon_url=ctx.author.avatar_url)

    progressionDates_message.set_thumbnail(url="https://media.discordapp.net/attachments/880157196141338705/"
                                               "895471020583055360/Progression_dates.jpg"
                                               "?width=1392&height=591")

    progressionDates_message.add_field(name="Progression Date Spreadsheet".title(),
                                       value="https://docs.google.com/spreadsheets/d/1y3GK_q1fOYUGrAZ_n4cbSXGRLKw"
                                             "-Ulub0-leGYlDaEA/edit#gid=0", inline=False)

    await ctx.send(embed=progressionDates_message)


@client.command()
async def command(ctx):
    """
    Defines the ability for a user to call '!command' in a channel and the bot will return a list of all command calls
    along with the description of each call

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: returns a message from the bot that has all the commands and their descriptions
    """
    command_message = discord.Embed(title="WagonCounter Command Help",
                                    description="Here is a list of the different bot commands that you may use to call on me!",
                                    color=bot_bar_color)

    # This shows the member who called the bot function
    command_message.set_author(name=ctx.author.display_name, url="https://deadrabbitsrdo.com",
                               icon_url=ctx.author.avatar_url)

    # Defines the contents of each field in the embed message
    command_message.add_field(name="!wagonSteals xx",
                              value="This command returns a list of 'wagon thieves' along with "
                                    "the amount of wagons each person has stolen. The xx is a "
                                    "value that must be entered by the user to tell the bot how"
                                    " many days you'd like to search back to see the score. ", inline=False)
    command_message.add_field(name="!bounties xx", value="This command returns a list of how many points each bounty "
                                                         "hunter has accumulated so far. 1 point is given for a bounty "
                                                         "brought in alive, 0.5 points for a bounty brought in dead.",
                              inline=False)

    command_message.add_field(name="!bountiesAlive xx", value="This command returns a list of how many bounties have"
                                                              " been turned in alive by each bounty hunter in the given "
                                                              "amount of days.", inline=False)

    command_message.add_field(name="!bountiesDead xx", value="This command returns a list of how many bounties have "
                                                             "been turned in dead by each bounty hunter in the given "
                                                             "amount of days.", inline=False)

    command_message.add_field(name="!members", value="This command returns a complete list of each user in the guild, "
                                                     "along with how many members are in each available role.",
                              inline=False)

    command_message.add_field(name="!eliteRanks",
                              value="This command returns all attainable titles in the guild, along with description "
                                    "of each rank, and how to earn them.", inline=False)
    command_message.add_field(name="!eliteRankProgress",
                              value="This command returns your progress toward the Elite Ranks. If you meet the "
                                    "requirements for one or more Elite Ranks and use this command, you will be given "
                                    "the roles for the Elite Ranks you have completed.", inline=False)
    command_message.add_field(name="!guide",
                              value="This command returns the Dead Rabbits Outlaw 101 - Survival Guide created by "
                                    "Bandit Blaggy#8895.", inline=False)

    command_message.add_field(name="!pvpGuide", value="This command returns the PVP Guide created by "
                                                      "BroomhildaChunks#0822.", inline=False)
    command_message.add_field(name="!wagonGuide", value="This command returns the Wonderful World of Wagon Thievery.",
                              inline=False)

    await ctx.send(embed=command_message)


@client.command()
async def pvpGuide(ctx):
    """
    Defines the ability for a user to call '!pvpGuide' in a channel and the bot will return Broom's PVP guide

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: a hyperlink to a website which contains the Broom's PVP guide
    """
    guide_message = discord.Embed(
        title="Broom's PVP Guide",
        url="https://docs.google.com/presentation/d/1i6Mdt0i_wkXgji7PqRz_02_lEKMvreQroCRX_J0LxbU/edit#slide=id"
            ".g101233f19a8_1_45", description="Click on the link to take you to the presentation.", color=bot_bar_color)

    # Displays the author of the PVP Guide
    guide_message.set_author(name="BroomhildaChunks#0822",
                             icon_url="https://cdn.discordapp.com/attachments/868317767818960978/924089703228129340/Logo.png")  # Change
    # this once Broom sends John his pic

    guide_message.set_thumbnail(
        url="https://cdn-longterm.mee6.xyz/plugins/commands/images/880151676588294234"
            "/0ca12f0ab76f5a896f3091f99d0e30c7a7378146e73832e5fe1ad0142f8994b1.jpeg")

    await ctx.send(embed=guide_message)


@client.command()
async def wagonGuide(ctx):
    """
    Defines the ability for a user to call '!wagonGuide' in a channel and the bot will return the Wagon Stealing Guide
    created by a member of the Dead Rabbits (author field)

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: a hyperlink to a website which contains the wagon clinic PowerPoint
    """
    guide_message = discord.Embed(title="Dead Rabbits RDO - Wagon Clinic",
                                  url="https://docs.google.com/presentation/d"
                                      "/19JE_pxvicWPNkucdqyi9BQzsZrVSKY7g1yDZ_DX86-0/edit#slide=id.p1",
                                  description="Click on the link to take you to the presentation.", color=bot_bar_color)

    # Displays the author of the Wagon Guide
    guide_message.set_author(name="_Sullynator_#5308",
                             icon_url="https://cdn.discordapp.com/attachments/937212866703007795/950515580774010880/"
                                      "John-L-Sullivan-1995-3x2gty-58b998a63df78c353cfc4456.jpg")

    guide_message.set_thumbnail(
        url="https://cdn-longterm.mee6.xyz/plugins/commands/images/880151676588294234"
            "/14c6d87f3d53fa724b84f37c51e12f75010da1fb72c1f26c1ca9c34d5c74b47e.png")

    await ctx.send(embed=guide_message)


@client.command()
async def wagonRefresh(ctx):
    """
    Defines the ability for a user to call '!wagonRefresh' in a channel and the bot will refresh the wagon counter.

    :param ctx: represents the context in which a command is being invoked under
    :type ctx: discord.ext.commands.context.Context
    :return: New name for the wagon counter name.
    """
    channel = await client.fetch_channel(wagon_counter_channel)
    print(start_num_days.days)

    wagon_steals_data = await CounterFunctionality.RedDeadRedemptionCounter().to_client(ctx, start_num_days.days)
    number_of_wagon_steals = CounterFunctionality.RedDeadRedemptionCounter().calculate()
    await channel.edit(name="Wagons Stolen: " + str(number_of_wagon_steals))


@client.command()
async def eliteRankProgress(ctx):
    """
    # TODO - Add description

    :param ctx: represents the context in which a command is being invoked under
    :return: An embed that displays a member's progress toward the Elite Ranks
    """
    # Reset all count & flag values
    hell_cat_maggie_wagon_steals_count = 0
    hell_cat_maggie_solo_no_kill_flag = "Incomplete"
    bondsman_alive_bounties_count = 0
    bondsman_dead_bounties_count = 0
    bondsman_max_bounty_flag = "Incomplete"
    bondsman_thrown_in_jail_flag = "Incomplete"
    roach_guard_parleys_count = 0
    roach_guard_content_defenses_count = 0

    # Retrieving information for the member who called the command
    command_target = ctx.author
    command_target_name = ctx.author.name
    command_target_icon = ctx.author.avatar_url
    command_target_roles = command_target.roles

    # Defining Elite Rank roles
    hell_cat_maggie_role = discord.utils.get(ctx.guild.roles, name="Hell-Cat Maggie")
    bondsman_role = discord.utils.get(ctx.guild.roles, name="Bondsman")
    roach_guard_role = discord.utils.get(ctx.guild.roles, name="Roach Guard")

    # Defining Wagon Counter channel
    wagon_counter_channel_id = 880186622375788614
    wagon_counter_channel = await client.fetch_channel(wagon_counter_channel_id)

    # Defining Bounty Counter channel
    bounty_counter_channel_id = 890970371698864208
    bounty_counter_channel = await client.fetch_channel(bounty_counter_channel_id)

    # Defining Parley Counter channel
    parley_counter_channel_id = 890970322612932648
    parley_counter_channel = await client.fetch_channel(parley_counter_channel_id)

    # Defining Announcement channel
    announcement_channel_id = 891350640989712424
    announcement_channel = await client.fetch_channel(announcement_channel_id)

    # Executes if target has all three Elite Rank roles. Creates an embed with a congratulatory message.
    if (hell_cat_maggie_role in command_target_roles) and (bondsman_role in command_target_roles) and \
            (roach_guard_role in command_target_roles):
        elite_ranks_complete = discord.Embed(
            description="Congratulations! You've already completed all the Elite Ranks.",
            color=bot_bar_color)

        await ctx.send(embed=elite_ranks_complete)

    # Executes if target does not have all three Elite Rank roles
    else:
        # Create header for the Elite Rank progress embed
        elite_rank_progress = discord.Embed(title="Elite Rank Progress for " + (str(command_target_name)),
                                            color=bot_bar_color)

        elite_rank_progress.set_author(name=command_target, icon_url=command_target_icon)

        # Executes if target has the Hell-Cat Maggie Role. Appends a message to the Elite Rank progress embed that the
        # target has already completed the role.
        if hell_cat_maggie_role in command_target_roles:  # Target has Hell-Cat Maggie role
            elite_rank_progress.add_field(name="Hell-Cat Maggie", value="Hell-Cat Maggie Elite Rank complete",
                                          inline=False)

        # Executes if target does not have the Hell-Cat Maggie role.
        else:
            # Gather the target's progress toward the role
            async for each_message in wagon_counter_channel.history(limit=None):
                if each_message.author == command_target:
                    if each_message.content == "drwagon":
                        hell_cat_maggie_wagon_steals_count += 1
                    if "solonokill" in each_message.content:
                        hell_cat_maggie_solo_no_kill_flag = "Complete"
            # If the target now meets the requirement(s) for the role, the role is given to the target
            if hell_cat_maggie_wagon_steals_count >= 100 and hell_cat_maggie_solo_no_kill_flag == "Complete":
                elite_rank_progress.add_field(name="Hell-Cat Maggie",
                                              value="Congratulations, you have now completed the requirements for the "
                                                    "Hell-Cat Maggie Elite Rank, and you have been given the role.",
                                              inline=False)

                await command_target.add_roles(hell_cat_maggie_role)

                # Build announcement message and post in #announcements channel
                hell_cat_maggie_complete_announcement = discord.Embed(
                    title="Hell-Cat Maggie Elite Rank Complete",
                    description=str(command_target_name) + " has completed the Hell-Cat Maggie Elite Rank!",
                    color=bot_bar_color)
                hell_cat_maggie_complete_announcement.set_image(
                    url="https://cdn.discordapp.com/attachments/924114659936710666/953079911990583316"
                        "/elite_rank_hellcat.png")
                await announcement_channel.send("@everyone")
                await announcement_channel.send(embed=hell_cat_maggie_complete_announcement)

            # If the target does not meet the requirement(s) for the role, their progress toward the role is displayed
            else:
                elite_rank_progress.add_field(name="Hell-Cat Maggie",
                                              value=str(
                                                  hell_cat_maggie_wagon_steals_count) + "/ 100 Wagon steals\nSolo, "
                                                                                        "no kill (include "
                                                                                        "screenshot): " + hell_cat_maggie_solo_no_kill_flag,
                                              inline=False)

        # Executes if target has the Bondsman Role. Appends a message to the Elite Rank progress embed that the target
        # has already completed the role.
        if bondsman_role in command_target_roles:
            elite_rank_progress.add_field(name="Bondsman", value="Bondsman Elite Rank complete", inline=False)

        # Executes if target does not have the Bondsman role
        else:
            # Gather the target's progress toward the role
            async for each_message in bounty_counter_channel.history(limit=None):
                if each_message.author == command_target:
                    if each_message.content == "dralive":
                        bondsman_alive_bounties_count = bondsman_alive_bounties_count + 1
                    if each_message.content == "drdead":
                        bondsman_dead_bounties_count = bondsman_dead_bounties_count + 1
                    if "maxbounty" in each_message.content:
                        bondsman_max_bounty_flag = "Complete"
                    if "timeserved" in each_message.content:
                        bondsman_thrown_in_jail_flag = "Complete"
            # If the target now meets the requirement(s) for the role, the role is given to the target
            if bondsman_alive_bounties_count >= 50 and bondsman_dead_bounties_count >= 50 and \
                    bondsman_max_bounty_flag == "Complete" and bondsman_thrown_in_jail_flag == "Complete":
                elite_rank_progress.add_field(name="Bondsman",
                                              value="Congratulations, you have now completed the requirements for the "
                                                    "Bondsman Elite Rank, and you have been given the role.",
                                              inline=False)
                await command_target.add_roles(bondsman_role)

                # Build announcement message and post in #announcements channel
                bondsman_complete_announcement = discord.Embed(title="Bondsman Elite Rank Complete",
                                                               description=str(
                                                                   command_target_name) + " has completed the Bondsman Elite Rank!",
                                                               color=bot_bar_color)
                bondsman_complete_announcement.set_image(
                    url="https://cdn.discordapp.com/attachments/924114659936710666/953079338985734184"
                        "/elite_rank_bondsman.png")
                await announcement_channel.send("@everyone")
                await announcement_channel.send(embed=bondsman_complete_announcement)

            # If the target does not meet the requirement(s) for the role, their progress toward the role is displayed
            else:
                elite_rank_progress.add_field(
                    name="Bondsman",
                    value=str(bondsman_alive_bounties_count) + " / 50 Alive bounties\n"
                          + str(bondsman_dead_bounties_count) + " / 50 Dead bounties\n"
                          + "Max bounty ($100, include screenshot): " + bondsman_max_bounty_flag + "\n"
                          + "Thrown in jail (include screenshot): " + bondsman_thrown_in_jail_flag, inline=False)

        # Executes if target has the Roach Guard Role. Appends a message to the Elite Rank progress embed that the
        # target has already completed the role.
        if roach_guard_role in command_target_roles:
            elite_rank_progress.add_field(name="Roach Guard", value="Roach Guard Elite Rank complete", inline=False)

        # Executes if target does not have the Roach Guard role
        else:
            # Gather the target's progress toward the role
            async for each_message in parley_counter_channel.history(limit=None):
                if each_message.author == command_target:
                    if each_message.content == "drparley":
                        roach_guard_parleys_count = roach_guard_parleys_count + 1
                    if each_message.content == "drdefense":
                        roach_guard_content_defenses_count = roach_guard_content_defenses_count + 1
            # If the target now meets the requirement(s) for the role, the role is given to them
            if roach_guard_parleys_count >= 50 and roach_guard_content_defenses_count >= 10:
                elite_rank_progress.add_field(
                    name="Roach Guard",
                    value="Congratulations, you have now completed the requirements for the Roach Guard Elite Rank, "
                          "and you have been given the role.", inline=False)
                await command_target.add_roles(roach_guard_role)
                # Build announcement message and post in #announcements channel
                roach_guard_complete_announcement = discord.Embed(
                    title="Roach Guard Elite Rank Complete",
                    description=str(command_target_name) + " has completed the Roach Guard Elite Rank!",
                    color=bot_bar_color)
                roach_guard_complete_announcement.set_image(
                    url="https://cdn.discordapp.com/attachments/924114659936710666/953078752793989190"
                        "/elite_rank_roach_guard.png")
                await announcement_channel.send("@everyone")
                await announcement_channel.send(embed=roach_guard_complete_announcement)

            # If the target does not meet the requirement(s) for the role, their progress towards the role is displayed
            else:
                elite_rank_progress.add_field(
                    name="Roach Guard",
                    value=str(roach_guard_parleys_count) + " / 50 Parleys\n"
                          + str(roach_guard_content_defenses_count) + " / 10 Content defenses",
                    inline=False)

        # Sends completed Elite Rank progress embed
        await ctx.send(embed=elite_rank_progress)


def get_all_members():
    """
    Gets each member in the guild, and puts them into a list
    :return: A list of users currently in the server
    """
    list_of_members = []  # Declaration of empty list

    # prints out each user in the guild
    for each_guild in client.guilds:
        for each_member in each_guild.members:
            list_of_members.append(str(each_member))  # adds the member

    remove_all_bots(list_of_members)

    return list_of_members


def remove_all_bots(list_of_members):
    """
    Removes all the bots recorded in the server
    
    :param list_of_members: a list of all members visible to the bot in the guild
    :type list_of_members: list
    :return: nothing
    """
    list_of_members.remove("Carl-bot#1536")
    list_of_members.remove("JB Cripps#8388")
    list_of_members.remove("JB Cripps#8388")
    list_of_members.remove("Statbot#3472")
    list_of_members.remove("GatorRed#9857")
    list_of_members.remove("PollBot Advanced#5365")
    list_of_members.remove("RDO Compendium#9528")
    list_of_members.remove("RDO Compendium#4808")
    list_of_members.remove("YAGPDB.xyz#8760")
    list_of_members.remove("Hydra#1214")
    list_of_members.remove("Hydra 2#9193")
    list_of_members.remove("ModMail#5460")
    list_of_members.remove("Kovop#9237")
    list_of_members.remove("Live Countdown#4463")
    list_of_members.remove("Battle Annie#4088")


signal.signal(signal.SIGTERM, lambda *_: client.loop.create_task(client.close()))
client.run(BOT_TOKEN)
