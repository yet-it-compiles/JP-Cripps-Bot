"""
# TODO -
"""

import datetime as dt


async def wagon_steals(ctx, days):
    """
    Sends the client a string representation of the names of the users along with their number of occurrences

    :param ctx: represents the context in which a command is being invoked under
    :param days: the number of days the user wants to search back in a channels message history
    :type days: int
    :return: A string of users vs. occurrences of wagon steals in descending order by name and occurrence
    """
    # Amount of days requested to search through
    time_interval = dt.datetime.utcnow() - dt.timedelta(days=int(days))

    # Declaration of dictionaries containing members vs. occurrences of the phrases
    dict_of_wagon_steelers = await build_dictionary(ctx, time_interval)

    # Sorts the occurrences and builds an output string
    sorted_occurrences = sorted(dict_of_wagon_steelers.items(), key=lambda x: x[1], reverse=True)

    list_output = build_output_string(sorted_occurrences)

    return list_output


async def build_dictionary(ctx, days):
    """
    Builds a dictionary of key/value pairs by iterating through a discords channels

    :param ctx: represents the context in which a command is being invoked under
    :param days: the number of days the user wants to search back in a channels message history
    :type days: int
    :return: a dictionary of each member along with the number of occurrences from the time frame specified
    """
    global users_vs_occurrences
    users_vs_occurrences = {}  # declares an empty dictionary

    # Defines logic for searching through a channels messages
    async for each_message in ctx.channel.history(limit=None, oldest_first=True, after=days):
        if is_target_phrase(each_message):  # if this message is a target message, assign the member to the dic. key
            member = each_message.author.name

            # Logic for adding new members into the dictionary and sets their occurrences to 0
            if member not in users_vs_occurrences:
                users_vs_occurrences[member] = 0

            # else they are already in the dictionary, and increment the amount of the users occurrences by 1
            users_vs_occurrences[member] = users_vs_occurrences[member] + 1

    return users_vs_occurrences


def is_target_phrase(message):
    """
    Determines if the message is 'drwagon' or not.

    :param message: each message visible in the channels' history
    :type message: str
    :return: a boolean value dependent on if the message is 'drwagon' or not
    """
    if 'drwagon' in message.content:
        return True
    else:
        return False


def build_output_string(dictionary_occurrences):
    """
    Creates the layout of the scoreboard of the member and the value associated

    :param dictionary_occurrences:  each member of the guild along with the number of times each said 'drwagon'
    :type dictionary_occurrences: dict
    :return: a string representation of the dictionary
    """
    helper_string = ""

    # Logic for how the dictionary should be printed
    for each_index, tuple in enumerate(dictionary_occurrences):
        wagon_stealers_name = tuple[0]
        number_of_steals = tuple[1]

        helper_string += wagon_stealers_name + ": " + str(number_of_steals) + "\n"
    return helper_string


def calculate():
    """
    Calculates the total number of values in the dictionary
    :return: the sum of values in the dictionary
    """
    counter = 0

    for each_value in users_vs_occurrences.values():
        counter += each_value

    return counter
