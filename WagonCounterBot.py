""" A module which defines how a user may call the bot to respond to specific commands, and then allows for each message
 to be embedded that is sent from the bot """

import os
import time
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import bhwagonCounter as wagonCounter

load_dotenv()  # loads the encapsulated values from the .env file

# Declaration of Encapsulated Variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
WAGON_CHANNEL = os.getenv('WAGON_STEAL_CHANNEL_KEY')

# Declaration Discord.py Variables
intents = discord.Intents.default()  # Turns on the connection
intents.members = True  # Ensures the member list will be updated properly
client = commands.Bot(command_prefix='!', intents=intents)  # defines the symbol used to call a command from the bot

# Declaration of Discord.py Variables
user_vs_occurrence = {}  # creates an empty dictionary , populated by on_ready


@client.event
async def on_ready():
    """ Sets the presence status of the bot when it first connects to the guild """
    await client.change_presence(activity=discord.Game('RDO - Wagon Stealing'))  # sets the bots Activity


@client.listen()
async def on_message(message):
    """
    Looks for when a member calls 'bhwagon', and after 24 minutes, sends them a message
    :param message: the message sent by the user
    :return: a DM to the user letting them know their cooldown ended
    """
    channel = client.get_channel(int(WAGON_CHANNEL))  # sets the

    if message.content.startswith("bhwagon"):
        channel = message.channel
        await cool_down_ended(message)


async def cool_down_ended(message):
    """
    Sends the author of the message a personal DM 24 minutes after they type 'bhwagon' in the guild
    :param message: is the message the author sent
    :return: a message to the author
    """
    time.sleep(1440)  # sets a time for 24 minutes = 1440 seconds

    await message.author.send("Your wagon steal timer is up 🎩 time for another materials run!")


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
    wagon_steals_data = await wagonCounter.wagon_steals(ctx, days)  # gets the dictionary v. occur. output list

    # Defines the name of the embed message along with the site to take a member to if they click on it
    wagon_steal_message = discord.Embed(
        title="Wagon Steals Counter",
        url="https://docs.google.com/spreadsheets/d/1or_UMRcmDrRPi1DyxbF0yYWOs7ujeW0qTmsf6nwrqPc/edit#gid=1230983397",
        color=0xFF5733)

    # Assigns the author field to the member who called the bot
    wagon_steal_message.set_author(name=ctx.author.display_name,
                                   url="https://www.blackhatsride.com",
                                   icon_url=ctx.author.avatar_url)

    # Determines which message to print based on the users passed in 'days' argument
    if int(days) > 1:
        wagon_steal_message.add_field(name=f"Top occurrences of 'bhwagon' in the last {days} days".title(),
                                      value=wagon_steals_data, inline=False)
        # wagonSteals.set_footer(text=f"Total number of steals in the last {days} days is {number_of_steals}")
    elif int(days) == 1:
        wagon_steal_message.add_field(name=f"Top occurrences of 'bhwagon' in the last day".title(),
                                      value=wagon_steals_data, inline=False)
        # wagonSteals.set_footer(text=f"Total number of steals in the last {days} day is {number_of_steals}")

    await ctx.send(embed=wagon_steal_message)


@client.command()
async def members(ctx):
    """
    Defines the ability for a user to call '!members' in a channel and the bot will return a list of all members
    organized into columns. The end of the message displays the total number of members in each role.
    :param ctx: represents the context in which a command is being invoked under
    :return: a complete list of members, the total amount in each role
    """
    all_members = get_all_members()  # list of all members
    all_members.sort(reverse=False)  # sorts the list in alphabetical order

    # defines guild role IDs
    owners = ctx.guild.get_role(813247048907751483)
    black_hats = ctx.guild.get_role(813926082960162866)
    prospectors = ctx.guild.get_role(822261499384037418)
    prospects = ctx.guild.get_role(861013512189116446)
    recruits = ctx.guild.get_role(813925577383084052)

    members_message = discord.Embed(
        title="Current Members List",
        url="https://www.blackhatsride.com/about-us",
        # description='-' + "\n-".join(all_members),
        color=0x4EEDEB)

    # This shows the member who called the bot function
    members_message.set_author(name=ctx.author.display_name,
                               url="https://www.blackhatsride.com",
                               icon_url=ctx.author.avatar_url)

    # Determines how many members to keep in each list
    length = len(all_members)  # 115

    # Separate the users into two Separate lists
    first_half = int((length // 2) - 15)
    second_half = first_half * 2

    first_half_members = all_members[0:first_half]
    second_half_members = all_members[first_half + 1:second_half]
    last_half_members = all_members[second_half + 1:length]

    # Shoes the title of each list
    members_message.add_field(name="Member List 1 ".title(), value=str("\n".join(first_half_members)), inline=True)
    members_message.add_field(name="Member List 2".title(), value=str("\n".join(second_half_members)), inline=True)
    members_message.add_field(name="Member List 3".title(), value=str("\n".join(last_half_members)), inline=True)

    # Shows the total amount of users in each role
    members_message.add_field(name="Current member count ".title(), value=str(len(all_members)), inline=True)
    members_message.add_field(name="Black Hat count ".title(), value=str(len(black_hats.members)), inline=True)
    members_message.add_field(name="Prospector count ".title(), value=str(len(prospectors.members)), inline=True)
    members_message.add_field(name="Prospect count ".title(), value=str(len(prospects.members)), inline=True)
    members_message.add_field(name="Recruit count ".title(), value=str(len(recruits.members)), inline=True)
    members_message.add_field(name="Owner count ".title(), value=str(len(owners.members)), inline=True)

    await ctx.send(embed=members_message)


@client.command()
async def guide(ctx):
    """
    Defines the ability for a user to call '!guide' in a channel and the bot will return a Survival Guide - Outlaw 101
    created by a member of the Black Hats (author field)
    :param ctx: represents the context in which a command is being invoked under
    :return: a hyperlink to a website which contains the Black Hats Survival Guide - Outlaw 101
    """

    guide_message = discord.Embed(
        title="Black Hat RDO Guide - Outlaw 101",
        url="https://docs.google.com/spreadsheets/d/1or_UMRcmDrRPi1DyxbF0yYWOs7ujeW0qTmsf6nwrqPc/edit#gid=34197895",
        description="This is the RDO Black Hats Guide, which will be helpful for new and veteran players alike. Feel "
                    "free to download a copy and use it as you wish!",
        color=0xE39DC2)

    # Displays the author of the Survival Guide
    guide_message.set_author(
        name="Katykinss#8895",
        url="https://www.twitch.tv/katymcblagg",
        icon_url="https://pbs.twimg.com/profile_images/1373717181276491780/vOus29er_400x400.jpg")
    await ctx.send(embed=guide_message)


# TODO - finish writing method
@client.command()
async def streamers(ctx):
    """
    Defines the ability for a user to call '!streamers' in a channel and the bot will return a list of all the streamers
    along with links to each of their channels
    :param ctx: represents the context in which a command is being invoked under
    :return: a hyperlink to a website which contains the survival guide - outlaw 101
    """
    streamers_message = discord.Embed(
        title="Black Hat RDO Guide - Outlaw 101",
        url="https://docs.google.com/spreadsheets/d/1or_UMRcmDrRPi1DyxbF0yYWOs7ujeW0qTmsf6nwrqPc/edit#gid=1230983397",
        description="This is the RDO Black Hats Guide, which will be helpful for new and veteran players alike. Feel "
                    "free to download a copy and use it as you wish!",
        color=0xE39DC2)

    streamers_message.set_author(name="Malthiel/xXMal911Xx",
                                 url="https://www.twitch.tv/realitybyt3s",
                                 icon_url="https://www.twitch.tv/realitybyt3s")


@client.command()
async def eliteRanks(ctx):
    """
    Defines the ability for a user to call '!eliteRanks' in a channel and the bot will return a list with descriptions
    of each attainable rank within the guild
    :param ctx: represents the context in which a command is being invoked under
    :return: a complete list of all possible roles the members may earn
    """
    elite_ranks_message = discord.Embed(
        title="Black Hat RDO - Elite Titles",
        url="https://docs.google.com/spreadsheets/d/1or_UMRcmDrRPi1DyxbF0yYWOs7ujeW0qTmsf6nwrqPc/edit#gid=1230983397",
        description="This is a list of the 'Elite Titles' that can be earned as described below ",
        color=0xFFDF00)

    # This shows the member who called the bot function
    elite_ranks_message.set_author(name=ctx.author.display_name,
                                   url="https://www.blackhatsride.com",
                                   icon_url=ctx.author.avatar_url)

    elite_ranks_message.add_field(name="The Honorable".title(),
                                  value="Given monthly to whichever Black Hat has accrued the most"
                                        " honor points for the month.", inline=False)
    elite_ranks_message.add_field(name="Wagon Whisperer".title(),
                                  value="Given Monthly to whichever Black Hat steals the most "
                                        "wagons in the month.", inline=False)
    elite_ranks_message.add_field(name="Wagon Chief".title(),
                                  value="This title, once earned stays with you. To earn this Elite "
                                        "Title, you must complete the following challenges: \n- Be a"
                                        " Full Black Hat. (Cannot be a recruit or prospect.) \n- 50 "
                                        "Wagons stolen as the Posse leader and documented in the "
                                        "Wagon Steal Counter channel. \n- Stolen a Wagon without "
                                        "killing anyone (Must be witnessed by at least two Black Hat"
                                        "s) \n- Stolen a Wagon solo. (Must be witnessed by at least "
                                        "two Black Hats. You may still posse up and announce the "
                                        "steal as usual, but the posse will remain in Valentine "
                                        "while the player pursuing the challenge completes the steal."
                                        ")"
                                  , inline=False)
    elite_ranks_message.set_footer(text="Notes: a single witness may be substituted for a video and/or stream")
    await ctx.send(embed=elite_ranks_message)


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
                               url="https://www.blackhatsride.com",
                               icon_url=ctx.author.avatar_url)

    # Defines the contents of each field in the embed message
    command_message.add_field(name="!wagonSteals xx", value="This command returns a list of 'wagon thiefs' along with "
                                                            "the amount of wagons each person has stolen. The xx is a "
                                                            "value that must be entered by the user to tell the bot how"
                                                            " many days you'd like to search back to see the score. "
                              , inline=False)
    command_message.add_field(name="!members",
                              value="This command returns a complete list of each user in the guild, along with how many"
                                    " members are in each available role.", inline=False)
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
    Removes all the bots recorded on the server
    :param list_of_members: a list of all members visible to the bot in the guild
    :return: nothing
    """
    list_of_members.remove("Carl-bot#1536")
    list_of_members.remove("Groovy#7254")
    list_of_members.remove("Rythm#3722")
    list_of_members.remove("Rythm 4#0952")
    list_of_members.remove("Rythm 3#0817")
    list_of_members.remove("Rythm 2#2000")
    list_of_members.remove("Rythm-chan#1001")
    list_of_members.remove("Statbot#3472")
    list_of_members.remove("YAGPDB.xyz#8760")
    list_of_members.remove("GatorRed#9857")
    list_of_members.remove("WagonCounter#8388")
    list_of_members.remove("WagonCounter#8388")
    list_of_members.remove("WordCounter#2462")
    list_of_members.remove("RDO Compendium#9528")


client.run(BOT_TOKEN)
