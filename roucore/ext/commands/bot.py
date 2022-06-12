import disnake
import typing as typ

class BaseBot(disnake.Client):
    """Base class for bots that uses RouCore
    """
    def __init__(self, *, text_command_prefix:str=None, text_case_insensetive:bool=False, owner_id:int=None, owner_ids:typ.Collection[int]=None, text_strip_after_prefix:bool=False, interactions_test_guilds:typ.List[int]=None, interactions_sync_commands:bool=True, interactions_sync_commands_on_cog_unload:bool=True, reload_on_changes:bool=False):
        pass # i implement it later

class RoucBot(BaseBot):
    pass
