import logging
import os

import interactions
from core.base import CustomClient
from dotenv import load_dotenv
from interactions import Extension
from interactions import InteractionContext
from interactions import listen
from interactions import OptionType
from interactions import slash_command
from interactions import slash_option
from interactions import SlashContext
from interactions.api.events import MessageReactionAdd
from interactions.api.events import MessageReactionRemove


load_dotenv()
test_guild_id = os.getenv("TEST_GUILD_ID")

DISALLOWED_ROLE_NAMES = ["admin"]


logging.basicConfig(
    filename="logs/interactions.log",
    level=logging.INFO,
    format="%(asctime)s UTC || %(levelname)s || %(message)s",
)


class RolesExtension(Extension):
    bot: CustomClient

    def __init__(self, bot):
        self.dict_of_guild_id_to_current_role_message = (
            {}
        )  # current role message is a message object. # todo save to pickle

    @slash_command(
        name="how-do-i-role-emoji",
        description="Instructions for how to create a role emoji reaction message",
    )
    async def how_do_i(self, ctx: SlashContext):
        await ctx.send(
            "Use /start-role-emoji-message to initialize the message, then use /add-role-to-message one or more times"
        )

    @slash_command(
        name="start-role-emoji-message",
        description="Create Role Assigning Message",
        #  scopes=[test_guild_id],
    )
    async def start_role_emoji_message(self, ctx: InteractionContext):
        current_role_message = await ctx.send("Role Emoji Reaction Message")
        self.dict_of_guild_id_to_current_role_message[
            ctx.guild.id
        ] = current_role_message

    @slash_command(name="add-role-to-message")
    @slash_option(
        name="role_name",
        description="Role Name",
        required=True,
        opt_type=OptionType.STRING,
    )
    @slash_option(
        name="emoji", description="Emoji", required=True, opt_type=OptionType.STRING
    )
    async def add_role_to_message(self, ctx: SlashContext, role_name: str, emoji: str):
        if role_name in DISALLOWED_ROLE_NAMES:
            raise ValueError  # todo give an error or warning message to user
        message_content = f"React with {emoji} to gain role {role_name}"
        if len(self.dict_of_guild_id_to_current_role_message.keys()) == 0:
            logging.error(
                "in extensions.roles, in add_role_to_message, len(self.dict_of_guild_id_to_current_role_message.keys()) == 0"
            )
            raise ValueError(
                "len(self.dict_of_guild_id_to_current_role_message.keys()) == 0"
            )
        current_role_message = self.dict_of_guild_id_to_current_role_message.get(
            ctx.guild.id
        )
        if current_role_message is None:
            raise ValueError("current_role_message is None")
        bot_message = current_role_message
        content = bot_message.content
        content += "\n" + message_content
        await bot_message.add_reaction(emoji)
        await bot_message.edit(content=content)
        await ctx.send(f"Role added", ephemeral=True)
        return
        pass  # todo add rolename and string to temporary structure

    @listen(MessageReactionAdd)
    async def on_message_reaction_add(
        self, reaction: interactions.api.events.MessageReactionAdd
    ):
        if reaction.author.id == self.bot.user.id:
            return
        if reaction.message.author.id != reaction.bot.user.id:
            return
        for role_name, emoji in get_role_and_emoji_from_message(
            reaction.message.content
        ):
            if role_name is None:
                continue
            if role_name in DISALLOWED_ROLE_NAMES:
                continue  # todo give error
            selected_role = None
            if emoji != reaction.emoji.name:
                continue  # todo error message
            for role in reaction.message.guild.roles:
                if role.name == role_name:
                    selected_role = role
            if selected_role is not None:
                await reaction.author.add_role(selected_role.id)
            else:
                logging.warning("on_message_reaction_add(): role_name not recognized")

    @listen(MessageReactionRemove)
    async def on_message_reaction_remove(
        self, reaction: interactions.api.events.MessageReactionRemove
    ):
        if reaction.author.id == self.bot.user.id:
            return
        if reaction.message.author.id != reaction.bot.user.id:
            return
        role_name = reaction.message.content.split()[-1]
        selected_role = None
        for role_name, emoji in get_role_and_emoji_from_message(
            reaction.message.content
        ):
            if role_name is None:
                continue
            if role_name in DISALLOWED_ROLE_NAMES:
                continue  # todo give error
            selected_role = None
            if emoji != reaction.emoji.name:
                continue  # todo error message
            for role in reaction.message.guild.roles:
                if role.name == role_name:
                    selected_role = role
            if selected_role is not None:
                await reaction.author.remove_role(selected_role.id)
            else:
                logging.warning(
                    "on_message_reaction_remove(): role_name not recognized"
                )


def setup(bot: CustomClient):
    """Let interactions load the extension"""

    RolesExtension(bot)


def get_role_and_emoji_from_message(content: str):
    """Takes content from the role emoji reaction message, which can look like the following:
    Role Emoji Reaction Message
    React with 🌞 to gain role new-role
    React with 👒 to gain role other-role
    """
    lines = content.split("\n")

    for line in lines:
        if not line.startswith("React"):
            continue
        try:
            t = line.split(" ")
            emoji = t[2]
            role_name = t[-1]
            assert role_name not in DISALLOWED_ROLE_NAMES
            yield role_name, emoji
        except IndexError:
            yield None, None
        except AssertionError:
            yield None, None
