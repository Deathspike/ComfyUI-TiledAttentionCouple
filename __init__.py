from .modules.integrations.impact_pack.detailer_provider import DetailerProvider
from .modules.providers.config_provider import ConfigProvider
from .modules.providers.tiled_provider import TiledProvider

NODE_CLASS_MAPPINGS = {
    "TiledAttentionCoupleImpactPackDetailer": DetailerProvider,
    "TiledAttentionCouplePrompt": ConfigProvider,
    "TiledAttentionCouple": TiledProvider,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TiledAttentionCoupleImpactPackDetailer": "Tiled Attention Couple (Impact Pack Detailer)",
    "TiledAttentionCouplePrompt": "Tiled Attention Couple (Config)",
    "TiledAttentionCouple": "Tiled Attention Couple",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
