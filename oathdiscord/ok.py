from typing import Any, Optional, Type
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.bot import PrefixType, _default
from discord.ext.commands.help import HelpCommand
from discord.app_commands import CommandTree
from discord.ext.commands._types import BotT
from discord import Intents


class Bot(commands.Bot):
    def __init__(
        self,
        command_prefix: PrefixType[BotT],
        *,
        help_command: HelpCommand | None = ...,
        tree_cls: type[CommandTree[Any]] = app_commands.CommandTree,
        description: str | None = None,
        intents: Intents,
        **options: Any
    ) -> None:
        super().__init__(
            command_prefix,
            help_command=help_command,
            tree_cls=tree_cls,
            description=description,
            intents=intents,
            **options
        )
