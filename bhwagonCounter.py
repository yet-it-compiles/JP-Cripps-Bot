""" A module which builds a dictionary of members based on the amount of occurrences found by iterating through a
guilds channels messages """

import datetime as dt


async def wagon_steals(ctx, days):
    """
    Defines the functionality for the bot to return a list of users and the number of times they've said 'bhwagon'
    :param ctx: represents the context in which a command is being invoked under
    :param days: the number of days the user wants to search back in a channels message history
    :return: an output string of occurrences of wagon stealers in descending order
    """
    # Date variables for amount of time to go back
    time_interval = dt.datetime.utcnow() - dt.timedelta(days=int(days))

    # Declaration of Dictionaries containing members vs. occurrences of the phrases
    dict_of_wagon_stealers = await build_dictionary(ctx, time_interval)

    # Sorts the occurrences and builds an output string
    sorted_occurrences = sorted(dict_of_wagon_stealers.items(), key=lambda x: x[1], reverse=True)

    list_output = build_output_string(sorted_occurrences)

    return list_output


async def build_dictionary(ctx, days):
    """
    Builds a dictionary, counting the occurrences of wagon for each user in a given timeframe
    :param ctx: represents the context in which a command is being invoked under
    :param days: the number of days the user wants to search back in a channels message history
    :return: a dictionary of each member along with the number of occurrences from the time frame specified
    """
    users_vs_occurrences = {}  # declares an empty dictionary

    # Defines logic for searching through a channels messages
    async for each_message in ctx.channel.history(limit=None, oldest_first=True, after=days):
        if is_target_phrase(each_message):  # if this message is a target message
            member = each_message.author.name

            # Logic for adding new members into the dictionary and sets their occurrences to 0
            if member not in users_vs_occurrences:
                users_vs_occurrences[member] = 0

            # else they are already in the dictionary, and increment the amount of this users occurrences by 1
            users_vs_occurrences[member] = users_vs_occurrences[member] + 1

    return users_vs_occurrences


def is_target_phrase(message):
    """
    Determines if the message from the channel is 'bhwagon'
    :param message: each message visible in the channels history
    :return: a true or false value dependant on if the message is 'bhwagon' or not
    """
    if 'drwagon' in message.content:
        return True
    else:
        return False


def build_output_string(dictionary_occurrences):
    """
    Defines how the list is going to print
    :param dictionary_occurrences:  each member of the guild along with the number of times each said 'bhwagon'
    :return: a list of users with the amount of occurrences of 'bhwagon'
    """
    helper_string = ""

    # Logic for how the dictionary should be printed
    for each_index, tuple in enumerate(dictionary_occurrences):
        wagon_stealers_name = tuple[0]
        number_of_steals = tuple[1]
        helper_string += wagon_stealers_name + ": " + str(number_of_steals) + "\n"
    return helper_string
