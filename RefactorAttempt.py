"""
This module contains the logic for each of the five counter functionalities. Each class is a subclass of RedDead-
RedemptionCounter which gives its subclasses structure. The only differences between each subclass is the way the target
phrases dictionary value is to be calculated.
"""

import datetime as dt


class RedDeadRedemptionCounter:
    """
    Creates a dictionary of users vs. amount of occurrences of a target phrase, orders it in descending order ands sends
    the information to the client
    """
    users_vs_occurrences = {}

    async def to_client(self, ctx, days):
        """
        Sends the client a string representation of the names of the users along with their number of occurrences

        :param ctx: represents the context in which a command is being invoked under
        :type ctx: discord.ext.commands.context.Context
        :param days: the number of days the user wants to search back in a channels message history
        :type days: str
        :return: A string of users vs. occurrences of wagon steals in descending order by name and occurrence
        """
        # Amount of days requested to search through
        time_interval = dt.datetime.utcnow() - dt.timedelta(days=int(days))

        # Declaration of dictionaries containing members vs. occurrences of the phrases
        dict_of_wagon_steelers = await self.build_dictionary(ctx, time_interval)

        # Sorts the occurrences and builds an output string
        sorted_occurrences = sorted(dict_of_wagon_steelers.items(), key=lambda x: x[1], reverse=True)

        list_output = self.build_output_string(sorted_occurrences)

        return list_output

    async def build_dictionary(self, ctx, days):
        """
        Builds a dict. assigning each member to its key, and the number of occurrences of target phrase to its value

        :param ctx: represents the context in which a command is being invoked under
        :type ctx: discord.ext.commands.context.Context
        :param days: the number of days the user wants to search back in a channels message history
        :type days: str
        :return: a dictionary of each member along with the number of occurrences from the time frame specified
        """
        global users_vs_occurrences
        self.users_vs_occurrences.clear()  # Ensures dictionary is clear before recomputing

        # Defines logic for searching through a channels messages
        async for each_message in ctx.channel.history(limit=None, oldest_first=True, after=days):
            if self.is_target_phrase(each_message):  # if message is target message, assign the member to the dic. key
                member = each_message.author.name

                # Logic for adding new members into the dictionary and sets their occurrences to 0
                if member not in self.users_vs_occurrences:
                    self.users_vs_occurrences[member] = 0

                # else they are already in the dictionary, and increment the amount of the users occurrences by 1
                self.users_vs_occurrences[member] = self.users_vs_occurrences[member] + 1

        return self.users_vs_occurrences

    def is_target_phrase(self, message):
        """
        Determines if the message is 'drwagon' or not.

        :param message: each message visible in the channels' history
        :type message: discord.message.Message
        :return: a boolean value dependent on if the message is 'drwagon' or not
        """
        if message.content == "drwagon":
            return True
        if message.content == "drdead":
            return True
        else:
            return False

    def decode_message(self, message):
        """
        Unwraps the message and returns it

        :param message: each message visible in the channels' history
        :type message: discord.message.Message
        :return: the content of the message
        """
        return message.content

    def build_output_string(self, dictionary_occurrences):
        """
        Creates the layout of the scoreboard from the dictionary

        :param dictionary_occurrences:  each member of the guild along with the number of times each said 'drwagon'
        :param dictionary_occurrences: list
        :return: a string representation of the dictionary
        """
        helper_string = ""

        # Logic for how the dictionary should be printed
        for each_index, tuple in enumerate(dictionary_occurrences):
            members_name = tuple[0]
            value_collected = tuple[1]

            helper_string += members_name + ": " + str(value_collected) + "\n"
        return helper_string

    def calculate(self):
        """
        Calculates the total number of values in the dictionary

        :return: the sum of values in the dictionary
        """
        counter = 0

        for each_value in self.users_vs_occurrences.values():
            counter += each_value

        return counter


class AliveCounter(RedDeadRedemptionCounter):
    """ Calculates the amount of bounties brought in alive and returns the dictionary to the client """

    def is_target_phrase(self, message):
        """
        Determines if the message is 'drwagon' or not.

        :param message: each message visible in the channels' history
        :type message: discord.message.Message
        :return: a boolean value dependent on if the message is 'drwagon' or not
        """
        if message.content == "dralive":
            return True
        else:
            return False


class BountiesCounter(RedDeadRedemptionCounter):
    """ Calculates the sum of both bounties brought in alive ,and dead then returns the dictionary to the client """
    user_vs_occurrences = {}

    async def build_dictionary(self, ctx, days):
        """
        Builds a dictionary, counting the occurrences of wagon for each user in a given timeframe
        :param ctx: represents the context in which a command is being invoked under
        :type ctx: discord.ext.commands.context.Context
        :param days: the number of days the user wants to search back in a channels message history
        :type days: str
        :return: a dictionary of each member along with the number of occurrences from the time frame specified
        """
        self.user_vs_occurrences.clear()  # ensures we are starting with a new dict

        # Defines logic for searching through a channels messages
        async for each_message in ctx.channel.history(limit=None, oldest_first=True, after=days):
            if self.is_target_phrase(each_message):  # if this message is a target message
                member = each_message.author.name
                message = self.decode_message(each_message)  # the message the user sent

                # Logic for adding new members into the dictionary and sets their occurrences to 0
                if member not in self.user_vs_occurrences:
                    self.user_vs_occurrences[member] = 0

                if message == 'dralive':
                    self.user_vs_occurrences[member] = self.user_vs_occurrences[member] + 1
                else:  # else the message is 'drdead' which = 0.5 pts
                    self.user_vs_occurrences[member] = self.user_vs_occurrences[member] + 0.5

        return self.user_vs_occurrences

    def is_target_phrase(self, message):
        """
        Determines if the message is 'drwagon' or not.

        :param message: each message visible in the channels' history
        :type message: discord.message.Message
        :return: a boolean value dependent on if the message is 'drwagon' or not
        """
        if message.content == "dralive":
            return True
        if message.content == "drdead":
            return True
        else:
            return False


class DeadCounter(RedDeadRedemptionCounter):
    """ Calculates the bounties brought in alive ,and dead then returns the dictionary to the client """
    user_vs_occurrences = {}

    async def build_dictionary(self, ctx, days):
        """
        Builds a dictionary, counting the occurrences of wagon for each user in a given timeframe
        :param ctx: represents the context in which a command is being invoked under
        :type ctx: discord.ext.commands.context.Context
        :param days: the number of days the user wants to search back in a channels message history
        :type days: str
        :return: a dictionary of each member along with the number of occurrences from the time frame specified
        """
        self.user_vs_occurrences.clear()  # ensures we are starting with a new dict

        # Defines logic for searching through a channels messages
        async for each_message in ctx.channel.history(limit=None, oldest_first=True, after=days):
            if self.is_target_phrase(each_message):  # if this message is a target message
                member = each_message.author.name
                message = self.decode_message(each_message)  # the message the user sent

                # Logic for adding new members into the dictionary and sets their occurrences to 0
                if member not in self.user_vs_occurrences:
                    self.user_vs_occurrences[member] = 0

                if each_message.content == "drdead":
                    self.user_vs_occurrences[member] = self.user_vs_occurrences[member] + 0.5

        return self.user_vs_occurrences

    def calculate(self):
        """
        Calculates the total number of values in the dictionary

        :return: the sum of values in the dictionary
        """
        counter = 0

        for each_value in self.user_vs_occurrences.values():
            counter += each_value

        return counter


class ParleyCounter(RedDeadRedemptionCounter):
    """ """
    def is_target_phrase(self, message):
        """
        Determines if the message is 'drwagon' or not.

        :param message: each message visible in the channels' history
        :type message: discord.message.Message
        :return: a boolean value dependent on if the message is 'drwagon' or not
        """
        if message.content == "drparley":
            return True
        else:
            return False