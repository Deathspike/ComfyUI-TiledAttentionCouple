from .modules.config_provider import ConfigProvider
from .modules.encoder_provider import EncoderProvider

NODE_CLASS_MAPPINGS = {
    "TiledAttentionCouplePrompt": ConfigProvider,
    "TiledAttentionCouple": EncoderProvider,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TiledAttentionCouplePrompt": "Tiled Attention Couple (Config)",
    "TiledAttentionCouple": "Tiled Attention Couple",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
