""" This module embeds the information sent to it within a message and sends it to the chat based on method specific
command calls. """
import asyncio
import os
import signal
import discord
import random

import RefactorAttempt
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # loads the encapsulated values from the .env file

# Declaration of Encapsulated Variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
WAGON_CHANNEL = os.getenv('WAGON_STEAL_CHANNEL_KEY')

# Declaration Discord.py Variables
intents = discord.Intents.default()  # Turns on the connection
intents.members = True  # Ensures the member list will be updated properly
client = commands.Bot(command_prefix='!', intents=intents)  # defines the symbol used to call a command from the bot


@client.event
async def on_ready():
    """ Sets the status of the bot when it connects to the guild """
    await client.change_presence(activity=discord.Game('RDO - Wagon Stealing'))  # sets the bots activity status


@client.listen()
async def on_message(message):
    """
    Listens for when a member calls 'drwagon', and after 24 minutes, sends them a message to the user
    :param message: the message sent by the user
    :return: a DM to the user letting them know their cooldown has ended
    """
    if message.content.startswith("drwagon"):
        await cool_down_ended(message)
    elif message.content.startswith("!"):
        await message.delete()


async def cool_down_ended(message):
    """
    Sends the author of the message a personal DM 24 minutes after they type 'drwagon' in a guild channel
    :param message: message the author sent
    :return: a message to the author letting them know they can wagon steal again
    """
    # Variables which store pictures messages
    picture1 = discord.File('Old Cripps Looking Weathered.png')
    picture2 = discord.File('Cripps Smoking.png')

    # Defines a list which stores quotes to send to the user
    list_of_quotes = \
        [
            "Your wagon steal timer is up 🎩\nLooks like it's time for another materials run!",
            f'Hey {message.author}, looks like our materials are running low again',
            'Did you get the telegram I sent you? \nWe need to get some more materials, so lets get out there and hit '
            'another wagon.',
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
            picture1, picture2

        ]

    await asyncio.sleep(1440)  # sets a time for 24 minutes = 1440 seconds
    response_to_send = random.choice(list_of_quotes)  # randomizes the the responses

    if response_to_send == picture1:
        await message.author.send(file=discord.File('Old Cripps Looking Weathered.png'))
    elif response_to_send == picture2:
        await message.author.send(file=discord.File('Cripps Smoking.png'))
    else:
        await message.author.send(response_to_send)


@client.event
async def on_reaction_add(reaction, user):  # reaction & user as an argument
    """
    Sends a message to a user 24 minutes later, after they react to a message
    :param reaction: '✅' - checkmark emoji/reaction
    :param user: is the member who reacted to the message
    :return: a message to the user letting them know their cool down is up
    """
    if reaction.emoji == '✅':  # See if the reaction is the same as in the code
        await asyncio.sleep(1440)  # sets a time for 24 minutes = 1440 seconds

        # Variables which store the pictures
        picture1 = discord.File('Old Cripps Looking Weathered.png')
        picture2 = discord.File('Cripps Smoking.png')

        # A list which stores the possible quotes to send to the user
        list_of_quotes = \
            [
                "Your wagon steal timer is up 🐇\nLooks like it's time for another materials run!",
                f'Hey {user}, looks like our materials are running low again',
                'Did you get the telegram I sent you? \nWe need to get some more materials, so lets get out there and '
                'hit '
                'another wagon.',
                "*A mailman walks up to you and hands you a letter..."
                "you open it, realizing it's from Cripps* "
                f"\n\nDear {user},\nI need more materials to keep our trade post running. \nBring some more "
                f"when you can.",
                f"It's huntin' time, {user}. Time to get on that horse!",
                "Look at Jay on that wagon list, you won't just let him top that leaderboard -that- easy, right? \nGet "
                "out there!",
                "Cops should be gone by now, already talked to the other Black Hats, we're just waiting on the call. "
                "Let's get out there again",
                "Did I ever tell you about the time.... wait the hell am I talkin to you for there are wagons need "
                "stealin!   And to think my Pa thought you'd be a no good trader all your life",
                "As much as I love our conversations.   Some poor bastard needs his wagon liberating from them.   "
                "Take the damn dog with you. Flea biten mongrel gives me all kinds of evils",
                "You know how Moses parted the Red Sea?   Well I can tell you like to part traders from their goods, "
                "and guess what time it is?",
                picture1, picture2
            ]

        response = random.choice(list_of_quotes)

        if response == picture1:
            await user.send(file=discord.File('Old Cripps Looking Weathered.png'))
        elif response == picture2:
            await user.send(file=discord.File('Cripps Smoking.png'))
        else:
            await user.send(response)


@client.command()
async def wagonSteals(ctx, days):
    """
    Defines a command which is called by typing '!wagonCounter xx' in any channel.
    The xx represents the amount of days look back through.
    NOTE: 'Read Message History' must be turn on in Channel Permissions
    :param ctx: represents the context in which a command is being invoked under
    :param days: the number of days a member wants to look back into a channels message history
    :return: an embedded message with a list of users and their number of occurrences of 'bhwagon'
    """

    wagon_steals_data = await RefactorAttempt.RedDeadRedemptionCounter().to_client(ctx, days)  # gets the dictionary v. occur. output list
    number_of_wagon_steals = RefactorAttempt.RedDeadRedemptionCounter().calculate()

    # Defines the name of the embed message along with the site to take a member to if they click on it
    wagon_steal_message = discord.Embed(
        title="Wagon Steals Counter",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        color=0xFF5733)

    # Assigns the author field to the member who called the bot
    wagon_steal_message.set_author(name=ctx.author.display_name,
                                   url="https://www.deadrabbitsrdo.com",
                                   icon_url=ctx.author.avatar_url)

    wagon_steal_message.set_thumbnail(url="https://media-rockstargames-com.akamaized.net/tina-uploads/posts"
                                          "/k498991k775ka8/0d8094e147c018ccd87c79294eedce3fcfcbb405.png")

    # Determines which message to print based on the users passed in 'days' argument
    if int(days) > 1:
        wagon_steal_message.add_field(name=f"Top Occurrences of 'drwagon' In The Last {days} Days",
                                      value=wagon_steals_data, inline=False)
        wagon_steal_message.set_footer(text=f"Total number of steals in the last {days} days is {number_of_wagon_steals}")
    elif int(days) == 1:
        wagon_steal_message.add_field(name=f"Top Occurrences of 'drwagon' In The Last Day",
                                      value=wagon_steals_data, inline=False)
        wagon_steal_message.set_footer(text=f"Total number of steals in the last {days} days is {number_of_wagon_steals}")

    await ctx.send(embed=wagon_steal_message)


@client.command()
async def bounties(ctx, days):
    """
    Defines a command which keeps track of the amount of points a player received by determined by weather or not they
    bring the bounty in dead or alive
    :param ctx: represents the context in which a command is being invoked under
    :param days: the number of days a member wants to look back into a channels message history
    :return: an embedded message with a list of users with the amount of points they've recieved from their bounties
    """
    bounties_recovered_data = await RefactorAttempt.BountiesCounter().to_client(ctx, days)
    total_bounties = RefactorAttempt.BountiesCounter().calculate()

    # Defines the embed header
    bounties_recovered = discord.Embed(
        title="Bounty Leader Board",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        color=0x2D95EB)

    # Displays the person who called the command
    bounties_recovered.set_author(name=ctx.author.display_name,
                                  url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    bounties_recovered.set_thumbnail(url="https://www.gamespot.com/a/uploads/screen_kubrick/1585/15855271/3765041"
                                         "-image004.png")

    # Logic to determine which embed message should send
    if int(days) > 1:
        bounties_recovered.add_field(name=f"Top Bounty Hunters in the last {days} days".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of bounties in the last {days} days is {total_bounties}")
    elif int(days) == 1:
        bounties_recovered.add_field(name=f"Top Bounty Hunters in the last {days} day".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of bounties in the last {days} day is {total_bounties}")
    await ctx.send(embed=bounties_recovered)


@client.command()
async def bountiesDead(ctx, days):
    bounties_recovered_data = await RefactorAttempt.DeadCounter().to_client(ctx, days)
    total_bounties = RefactorAttempt.DeadCounter().calculate()

    bounties_recovered = discord.Embed(
        title="Bounty Leader Board",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        color=0x2D95EB)

    bounties_recovered.set_author(name=ctx.author.display_name,
                                  url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    bounties_recovered.set_thumbnail(url="https://www.gamespot.com/a/uploads/screen_kubrick/1585/15855271/3765041"
                                         "-image004.png")

    if int(days) > 1:
        bounties_recovered.add_field(name=f"Number of Dead Bounties Brought in the last {days} days".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of dead bounties recovered in the last {days} days is {total_bounties}")
    elif int(days) == 1:
        bounties_recovered.add_field(name=f"Number of Dead Bounties Brought in the last day".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of dead bounties recovered in the last {days} day is {total_bounties}")
    await ctx.send(embed=bounties_recovered)


@client.command()
async def bountiesAlive(ctx, days):
    bounties_recovered_data = await RefactorAttempt.AliveCounter().to_client(ctx, days)  # gets the dictionary output list
    total_bounties = RefactorAttempt.AliveCounter().calculate()

    bounties_recovered = discord.Embed(
        title="Bounty Leader Board",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        color=0x2D95EB)

    bounties_recovered.set_author(name=ctx.author.display_name,
                                  url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    bounties_recovered.set_thumbnail(
        url="https://www.gamespot.com/a/uploads/screen_kubrick/1585/15855271/3765041-image004.png")

    if int(days) > 1:
        bounties_recovered.add_field(name=f"Number of Living Bounties Brought in the last {days} days".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of living bounties in the last {days} days is {total_bounties}")
    elif int(days) == 1:
        bounties_recovered.add_field(name=f"Number of Living Bounties Brought in the last day".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of living bounties in the last {days} day is {total_bounties}")
    await ctx.send(embed=bounties_recovered)


@client.command()
async def parley(ctx, days):
    bounties_recovered_data = await RefactorAttempt.ParleyCounter().to_client(ctx, days)  # gets the dictionary output list
    total_parleys = RefactorAttempt.ParleyCounter().calculate()

    bounties_recovered = discord.Embed(
        title="Bounty Leader Board",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        color=0x1BF761)

    bounties_recovered.set_author(name=ctx.author.display_name,
                                  url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    bounties_recovered.set_thumbnail(url="https://preview.redd.it/hzzvz0gi0j121.jpg?auto=webp&s"
                                         "=86411716d80ffc4516a2829ea362883ebc0ef36a")

    if int(days) > 1:
        bounties_recovered.add_field(name=f"Number of Parleys in the last {days} days".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of parleys in the last {days} days is {total_parleys}")
    elif int(days) == 1:
        bounties_recovered.add_field(name=f"Number of Parleys in the last day".title(),
                                     value=bounties_recovered_data, inline=False)
        bounties_recovered.set_footer(text=f"Total number of parleys in the last {days} day is {total_parleys}")
    await ctx.send(embed=bounties_recovered)


@client.command()
async def members(ctx):
    """
    Defines the ability for a user to call '!members' in a channel and the bot will return a list of all members
    organized into two columns. The end of the message displays the total number of members in each role.
    :param ctx: represents the context in which a command is being invoked under
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
    members_message = discord.Embed(
        title="\tCurrent Members List",
        url="https://deadrabbitsrdo.com",
        color=0x4EEDEB)

    # This shows the member who called the bot function
    members_message.set_author(name=ctx.author.display_name,
                               url="https://deadrabbitsrdo.com",
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
    :return: a hyperlink to a website which contains the Black Hats Survival Guide - Outlaw 101
    """
    guide_message = discord.Embed(
        title="Dead Rabbits RDO Guide - Outlaw 101",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        description="This is the RDO Dead Rabbits Guide, which will be helpful for new and veteran players alike. Feel "
                    "free to download a copy and use it as you wish!",
        color=0xE39DC2)

    # Displays the author of the Survival Guide
    guide_message.set_author(
        name="Katykinss#8895",
        url="https://www.twitch.tv/katymcblagg",
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
    :return: a complete list of all possible roles the members may earn
    """
    server_ranks_message = discord.Embed(
        title="Dead Rabbits RDO - Server Titles",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        description="A complete list of the available Server Titles",
        color=0x008080)

    # This shows the member who called the bot function
    server_ranks_message.set_author(name=ctx.author.display_name,
                                    url="https://deadrabbitsrdo.com",
                                    icon_url=ctx.author.avatar_url)

    server_ranks_message.set_thumbnail(
        url="https://github.com/yet-it-compiles/Wagon-Counter-Bot/blob/main/Ranks_and_titles.jpg?raw=true")

    server_ranks_message.add_field(name="Wanderer".title(),
                                   value="The base role of the server. All members joining the server will receive this "
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
    server_ranks_message.add_field(name="Dead Rabbit".title(),
                                   value="Members will progress to this rank upon completion of their membership "
                                         "checklist, concurrence of their sponsor, and completion of initiations. Dead "
                                         "Rabbits are full members of the crew. They are the most loyal and trusted "
                                         "members. Dead Rabbits have access to additional channels in the server and "
                                         "are eligible for Elite Ranks. ", inline=False)

    server_ranks_message.set_footer(text="Membership checklist is maintained by the sponsor.")

    await ctx.send(embed=server_ranks_message)


@client.command()
async def inGameRankTitles(ctx):
    """
    Defines the ability for a user to call '!serverRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild
    :param ctx: represents the context in which a command is being invoked under
    :return: a complete list of all possible roles the members may earn
    """
    inGameRankTitles_message = discord.Embed(
        title="Dead Rabbits RDO - In-Game Rank Titles",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        description="A complete list of the available In-Game Rank Titles",
        color=0x008080)

    # This shows the member who called the bot function
    inGameRankTitles_message.set_author(name=ctx.author.display_name,
                                        url="https://deadrabbitsrdo.com",
                                        icon_url=ctx.author.avatar_url)

    inGameRankTitles_message.set_thumbnail(url="https://github.com/yet-it-compiles/Wagon-Counter-Bot/blob/main"
                                               "/Ranks_and_titles.jpg?raw=true")

    inGameRankTitles_message.add_field(name="Plug Ugly: 0-99".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="Day Breaker: 100-199".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="200-299: Night Walker".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="300-399: Black Bird".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="400-499: Slaughter Houser".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="500-599: Broadway Twister".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="600-699: Bloody Sixther".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="700-799: Autumn Diver".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="800-899: Battle Annie".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="900-999: 40 Thieves".title(),
                                       value="-",
                                       inline=False)

    inGameRankTitles_message.add_field(name="1000+: Know Nothing".title(),
                                       value="-",
                                       inline=False)

    await ctx.send(embed=inGameRankTitles_message)


@client.command()
async def monthlyEliteRanks(ctx):
    """
    Defines the ability for a user to call '!serverRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild
    :param ctx: represents the context in which a command is being invoked under
    :return: a complete list of all possible roles the members may earn
    """
    monthlyEliteRanks_message = discord.Embed(
        title="Dead Rabbits RDO - Monthly Elite Ranks",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        description="A complete list of the available Monthly Elite Ranks",
        color=0x008080)

    # This shows the member who called the bot function
    monthlyEliteRanks_message.set_author(name=ctx.author.display_name,
                                         url="https://deadrabbitsrdo.com",
                                         icon_url=ctx.author.avatar_url)

    monthlyEliteRanks_message.set_thumbnail(
        url="https://github.com/yet-it-compiles/Wagon-Counter-Bot/blob/main/Ranks_and_titles.jpg?raw=true")

    monthlyEliteRanks_message.add_field(name="Highwayman".title(),
                                        value="Awarded monthly to whoever leads the most wagon steals. Steals for this "
                                              "award must be performed on the server. Credit goes to whoever spotted the "
                                              "wagon.", inline=False)
    monthlyEliteRanks_message.add_field(name="Butcher".title(),
                                        value=" Awarded monthly to whoever has made the most griefers quit. Quitting is "
                                              "defined as the player(s) parley, leave session, fast travel away or hide in a "
                                              "safe zone. If they hide or fast travel, you must wait for two minutes and "
                                              "verify they do not return to fight. Must be performed on the server. Any "
                                              "member of the posse may claim credit. Salty players after content do not "
                                              "count as griefers.", inline=False)
    monthlyEliteRanks_message.add_field(name="Recovery Agent".title(),
                                        value="Awarded monthly to whoever has earned the most points for player bounties. "
                                              "Alive: 1 point\n    Dead: 1/2 point\n    "
                                              "Submissions to the bounty counter must be accompanied by a screenshot of the "
                                              "Bounty Complete screen. May be performed solo or in a posse. Does not have "
                                              "to be performed on the server, but is preferred. ", inline=False)

    monthlyEliteRanks_message.add_field(name="Recovery Agent".title(),
                                        value="Awarded monthly to whoever has earned the most points for player bounties. "
                                              "Alive: 1 point\n    Dead: 1/2 point\n    "
                                              "Submissions to the bounty counter must be accompanied by a screenshot of the "
                                              "Bounty Complete screen. May be performed solo or in a posse. Does not have "
                                              "to be performed on the server, but is preferred. ", inline=False)

    monthlyEliteRanks_message.add_field(name="Priest".title(),
                                        value="Awarded Monthly to whoever has earned the most honor as awarded by the "
                                              "membership in the #honor-counter.", inline=False)

    await ctx.send(embed=monthlyEliteRanks_message)


@client.command()
async def eliteRanks(ctx):
    """
    Defines the ability for a user to call '!serverRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild
    :param ctx: represents the context in which a command is being invoked under
    :return: a complete list of all possible roles the members may earn
    """
    eliteRanks_message = discord.Embed(
        title="Dead Rabbits RDO - Elite Ranks",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        description="A complete list of the available Elite Rank Titles",
        color=0x008080)

    # This shows the member who called the bot function
    eliteRanks_message.set_author(name=ctx.author.display_name,
                                  url="https://deadrabbitsrdo.com",
                                  icon_url=ctx.author.avatar_url)

    eliteRanks_message.set_thumbnail(
        url="https://github.com/yet-it-compiles/Wagon-Counter-Bot/blob/main/Ranks_and_titles.jpg?raw=true")

    eliteRanks_message.add_field(name="Hell-Cat Maggie".title(),
                                 value="Love stealing wagons? This Rank goes to any member that has lead 100 "
                                       "wagon steals as tracked in the Wagon Steal Counter, and has performed "
                                       "at "
                                       "least one of them solo without killing anyone. The Solo No Kill steal "
                                       "must be witnessed by a full Dead Rabbit. Any steals led while a "
                                       "Wanderer "
                                       "or Short Tail will count towards the total.", inline=False)

    eliteRanks_message.add_field(name="Roach Guard".title(),
                                 value="These are the most feared and ruthless members of the crew when it comes to "
                                       "PvP. This Rank goes to members who have documented 50 Parleys in the counter, "
                                       "and have Defended the crew 10 times during content. (Content can be anything "
                                       "from a rival trader attempting to steal a wagon, a player bounty, or hostile "
                                       "players attacking a free roam mission.)", inline=False)

    eliteRanks_message.add_field(name="Bondsman".title(),
                                 value="Criminals flee from them. This rank goes to members who have met the "
                                       "following criteria: "
                                       "50 player bounties brought in alive    50 player bounties brought in dead    "
                                       "Achieved max player bounty of $100 with screenshot as proof "
                                       "    Been turned in to jail with screenshot as proof", inline=False)

    eliteRanks_message.add_field(name="Five Pointer".title(),
                                 value="The Moderators of the crew. They have the authority and ability to mute, "
                                       "and deafen members should the rare need arise.", inline=False)

    await ctx.send(embed=eliteRanks_message)


@client.command()
async def dates(ctx):
    """
    Defines the ability for a user to call '!serverRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild
    :param ctx: represents the context in which a command is being invoked under
    :return: a complete list of all possible roles the members may earn
    """
    progressionDates_message = discord.Embed(
        title="Dead Rabbits RDO - Wanderer Progression Dates",
        url="https://docs.google.com/spreadsheets/d/1K-bY3MriRt1Qm4CP-6odIf-0CA2Rc8l-IMlSVmjMj6g/edit#gid=837843276",
        description="A helpful resource to view the progression dates for new members",
        color=0x32a869)

    # This shows the member who called the bot function
    progressionDates_message.set_author(name=ctx.author.display_name,
                                        url="https://deadrabbitsrdo.com",
                                        icon_url=ctx.author.avatar_url)

    progressionDates_message.set_thumbnail(
        url="https://media.discordapp.net/attachments/880157196141338705/895471020583055360/Progression_dates.jpg?width=1392&height=591")

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
    :return: returns a message from the bot that has all the commands and their descriptions
    """
    command_message = discord.Embed(
        title="WagonCounter Command Help",
        description="Here is a list of the different bot commands that you may use to call on me!",
        color=0xF70C1C)

    # This shows the member who called the bot function
    command_message.set_author(name=ctx.author.display_name,
                               url="https://deadrabbitsrdo.com",
                               icon_url=ctx.author.avatar_url)

    # Defines the contents of each field in the embed message
    command_message.add_field(name="!wagonSteals xx", value="This command returns a list of 'wagon thiefs' along with "
                                                            "the amount of wagons each person has stolen. The xx is a "
                                                            "value that must be entered by the user to tell the bot how"
                                                            " many days you'd like to search back to see the score. "
                              , inline=False)
    command_message.add_field(name="!bounties xx",
                              value="This command returns a list of how many points each bounty hunter has accumulated "
                                    "so far. 1 point is given for a bounty brought in alive, 0.5 points for a bounty "
                                    "brought in dead."
                              , inline=False)

    command_message.add_field(name="!bountiesAlive xx",
                              value="This command returns a list of how many bounties have been turned in alive by "
                                    "each bounty hunter in the given amount of days"
                              , inline=False)

    command_message.add_field(name="!bountiesDead xx",
                              value="This command returns a list of how many bounties have been turned in dead by "
                                    "each bounty hunter in the given amount of days"
                              , inline=False)

    command_message.add_field(name="!members",
                              value="This command returns a complete list of each user in the guild, along with how "
                                    "many members are in each available role.", inline=False)
    command_message.add_field(name="!guide",
                              value="This command returns the Black Hat Outlaw 101 - Survival Guide created by "
                                    "Katykinss#8895.", inline=False)
    command_message.add_field(name="!eliteRanks", value="This command returns all attainable titles in the guild, along"
                                                        " with description of each rank, and how to earn them.",
                              inline=False)

    await ctx.send(embed=command_message)


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
    :return: nothing
    """
    list_of_members.remove("Carl-bot#1536")
    list_of_members.remove("JB Cripps#8388")
    list_of_members.remove("JB Cripps#8388")
    list_of_members.remove("Statbot#3472")
    list_of_members.remove("GatorRed#9857")
    list_of_members.remove("PollBot Advanced#5365")
    list_of_members.remove("RDO Compendium#9528")
    list_of_members.remove("YAGPDB.xyz#8760")
    list_of_members.remove("Hydra#1214")
    list_of_members.remove("Hydra 2#9193")
    list_of_members.remove("ModMail#5460")
    list_of_members.remove("Kovop#9237")
    list_of_members.remove("Live Countdown#4463")


signal.signal(signal.SIGTERM, lambda *_: client.loop.create_task(client.close()))
client.run(BOT_TOKEN)
