""" A module which builds a dictionary of members based on the amount of occurrences found by iterating through a
guilds channels messages """

import datetime as dt


async def wagon_steals(ctx, days):
    """
    Defines the functionality for the bot to return a list of users and the number of times they've said 'bhwagon'
    :param ctx: represents the context in which a command is being invoked under
    :param days: the number of days the user wants to search back in a channels message history
    :return: an output string of occurrences in descending order
    """
    # Date variables for amount of time to go back
    after_date = dt.datetime.utcnow() - dt.timedelta(days=int(days))
    dictionary = await build_dictionary(ctx, after_date)  # dictionary with users and phrase occurrences

    # Sorts the occurrences and builds an output string
    sorted_occurrences = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

    list_output = build_output_string(sorted_occurrences)

    return list_output


def build_output_string(dictionary_occurrences):
    """
    Defines how the list is going to print
    :param dictionary_occurrences:  each member of the guild along with the number of times each said 'bhwagon'
    :return: a list of users with the amount of occurrences of 'bhwagon'
    """
    helper_string = ""

    # Logic for how the dictionary should be printed
    for each_index, tuple in enumerate(dictionary_occurrences):
        name = tuple[0]
        number = tuple[1]
        helper_string += name + ": " + str(number) + "\n"
    return helper_string


async def build_dictionary(ctx, days):
    """
    Builds a dictionary, counting the occurrences of wagon for each user in a given timeframe
    :param ctx: represents the context in which a command is being invoked under
    :param days: the number of days the user wants to search back in a channels message history
    :return: a dictionary of each member along with the number of occurrences from the time frame specified
    """
    dictionary = {}  # declares an empty dictionary

    # Defines logic for searching through a channels messages
    async for each_message in ctx.channel.history(limit=None, oldest_first=True, after=days):
        if is_target_phrase(each_message):  # if this message is 'bhwagon'
            wagon_stealer = each_message.author.name

            # Logic for adding new members into the dictionary and sets their occurrences to 0
            if wagon_stealer not in dictionary:
                dictionary[wagon_stealer] = 0

            # else they are already in the dictionary, and increment the amount of this users occurrences by 1
            dictionary[wagon_stealer] = dictionary[wagon_stealer] + 1
    return dictionary


def is_target_phrase(message):
    """
    Determines if the message from the channel is 'bhwagon'
    :param message: each message visible in the channels history
    :return: a true or false value dependant on if the message is 'bhwagon' or not
    """
    if 'bhwagon' in message.content:
        return True
    else:
        return False
