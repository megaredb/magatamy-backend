import enum

from backend.utils import config


class ServerEnum(enum.StrEnum):
    """
    vanilla-plus, vanilla
    """

    VanillaPlus = "vanilla-plus"


SERVERS = {ServerEnum.VanillaPlus: config.MAIN_MC_SERVER_HOST}
