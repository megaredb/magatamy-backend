import enum

from utils import config


class ServerEnum(enum.StrEnum):
    """
    vanilla-plus, vanilla
    """

    VanillaPlus = "vanilla-plus"
    Vanilla = "vanilla"


SERVERS = {
    ServerEnum.VanillaPlus: config.MAIN_MC_SERVER_HOST,
    ServerEnum.Vanilla: config.SECOND_MC_SERVER_HOST,
}
