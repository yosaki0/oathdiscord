from typing import Any, Optional, Type
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.help import HelpCommand
from discord.app_commands import CommandTree
from discord.ext.commands._types import BotT
from discord import Intents
from typing import NewType
from discord.abc import Snowflake
import aiohttp
from typing import Union
import requests

ClientId = NewType("ClientId", str)
ClientSecret = NewType("ClientSecret", str)


class OauthAppCommandPermissions:
    def __init__(self, id: Snowflake, type: int, permission: bool):
        """

        args:
            id Snowflake:
            type (int): 1(role)  2(user)  3(channel)
            permission (bool): set the permission on[true] or off[false]
        """
        self.id = str(id)
        if not type in [1, 2, 3]:
            raise ValueError('Invalid value for "type" argument.')
        self.type = type
        self.permission = permission

    def to_dict(self) -> dict:
        return {"id": self.id, "type": self.type, "permission": self.permission}


class OauthAppConnections:
    def __init__(
        self,
        type: str = None,
        id: str = None,
        name: str = None,
        visibility: int = None,
        friend_sync: bool = None,
        show_activity: bool = None,
        verified: bool = None,
        two_way_link: bool = None,
        metadata_visibility: int = None,
    ):
        self.type = type
        self.id = id
        self.name = name
        self.visibility = visibility
        self.friend_sync = friend_sync
        self.show_activity = show_activity
        self.verified = verified
        self.two_way_link = two_way_link
        self.metadata_visibility = metadata_visibility

    def __repr__(self) -> str:
        return f"<OauthAppConnections(type={self.type})>"


class OauthAppCommandsOption:
    def __init__(
        self,
        type: int,
        name: str,
        description: str,
        required: bool = False,
        choices: list[dict[str, int]] = None,
    ):
        self.type = type
        self.name = name
        self.description = description
        self.required = required
        self.choices = choices


class OauthAppCommand:
    __repr: int = False

    @classmethod
    def enable_repr(cls):
        cls.__repr = True

    def __init__(
        self,
        id: str = None,
        application_id: str = None,
        version: str = None,
        default_permission: bool = None,
        default_member_permissions: None = None,
        type: int = None,
        nsfw: bool = None,
        name: str = None,
        description: str = None,
        dm_permission: bool = None,
        options: list[dict[str, Union[int, str, bool]]] = None,
        repr: bool = False,
    ):
        self.id = id
        self.application_id = application_id
        self.version = version
        self.default_permission = default_permission
        self.default_member_permissions = default_member_permissions
        self.type = type
        self.nsfw = nsfw
        self.name = name
        self.description = description
        self.dm_permission = dm_permission
        if options != None:
            self.options = [OauthAppCommandsOption(**option) for option in options]
        else:
            self.options = options
        if repr:
            self.enable_repr()

    def __repr__(self):
        if self.__repr:
            return (
                f"JSONClass(id='{self.id}', application_id='{self.application_id}', version='{self.version}', "
                f"default_permission={self.default_permission}, default_member_permissions={self.default_member_permissions}, "
                f"type={self.type}, nsfw={self.nsfw}, name='{self.name}', description='{self.description}', "
                f"dm_permission={self.dm_permission}, options={self.options})"
            )
        return f"{self.__class__}"


class OauthAppCommandDone:
    def __init__(self, id: str, application_id: str, guild_id: str, permissions: list[dict]):
        self.id = id
        self.app_id = application_id
        self.guild_id = guild_id
        self.permissions = [OauthAppCommandPermissions(**perms) for perms in permissions]


class OaBot(commands.Bot):
    def __init__(
        self,
        command_prefix: BotT,
        *,
        help_command: HelpCommand | None = ...,
        tree_cls: type[CommandTree[Any]] = app_commands.CommandTree,
        description: str | None = None,
        intents: Intents,
        bearer_token: str = None,
        client_details: tuple[ClientId, ClientSecret] = None,
        token: str = None,
        **options: Any,
    ) -> None:
        self.bearer_token = bearer_token
        self.client_id = client_details[0]
        self.client_secret = client_details[1]
        self.bot_token = token
        self._base_url = "https://discord.com/api/v10/applications/%s"
        self._headers = {}

        super().__init__(
            command_prefix,
            help_command=help_command,
            tree_cls=tree_cls,
            description=description,
            intents=intents,
            **options,
        )

    async def edit_app_command_perms(
        self,
        guild_id: str,
        command_id: str,
        permissions: list[OauthAppCommandPermissions],
    ):
        url = self._base_url % (
            f"{self.client_id}/guilds/{guild_id}/commands/{command_id}/permissions"
        )
        self._headers["Authorization"] = f"Bearer {self.bearer_token}"
        json_data = {"permissions": []}

        for perms in permissions:
            if not isinstance(perms, OauthAppCommandPermissions):
                raise TypeError("invalid permissions type")
            json_data["permissions"].append(perms.to_dict())

        async with aiohttp.ClientSession() as session:
            request = await session.put(url, headers=self._headers, json=json_data)
            request_json = await request.json()
            
        if request.status == 200:
            return OauthAppCommandDone(**request_json)
        
        elif request.status == 401:
            raise discord.Forbidden(request_json["message"])
        
        else:
            raise discord.HTTPException(request, message=request_json["message"])