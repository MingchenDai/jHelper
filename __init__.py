from nonebot.plugin import PluginMetadata, get_plugin_config

from .config import Config

__plugin_meta__=PluginMetadata(
    name="jHelper",
    descripition="Python helper for Shanghai Jiao Tong University",
    usage="",
    homepage="https:github.com/MingchenDai/jHelper",
    type="application",
    config=Config,
    extra={},
    supported_adapters=set(),
)