from .tiled_attention_couple_config import TiledAttentionCoupleConfig


class TiledAttentionCouplePrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "division": ("STRING", {"default": "1,1"}),
                "orientation": (["horizontal", "vertical"],),
                "positive": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "negative": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            }
        }

    CATEGORY = "conditioning"
    FUNCTION = "process"
    RETURN_TYPES = ("TILED_CONFIG",)

    def process(self, division, orientation, positive, negative):
        division = [float(x.strip()) for x in division.split(",")]
        positive_base, positive_tiles = parse_text(positive)
        negative_base, negative_tiles = parse_text(negative)
        return (
            TiledAttentionCoupleConfig(
                division,
                orientation,
                positive_base,
                positive_tiles,
                negative_base,
                negative_tiles,
            ),
        )


def parse_text(value):
    parts = [part.strip() for part in value.split("BREAK")]
    tiles = parts[1:] if len(parts) > 1 else []
    return (parts[0], tiles)
