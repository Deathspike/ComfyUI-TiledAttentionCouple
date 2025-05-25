from .tiled_attention_couple import TiledAttentionCouple
from .tiled_attention_couple_prompt import TiledAttentionCouplePrompt

NODE_CLASS_MAPPINGS = {
    "TiledAttentionCouple": TiledAttentionCouple,
    "TiledAttentionCouplePrompt": TiledAttentionCouplePrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TiledAttentionCouple": "Tiled Attention Couple",
    "TiledAttentionCouplePrompt": "Tiled Attention Couple (Prompt)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
