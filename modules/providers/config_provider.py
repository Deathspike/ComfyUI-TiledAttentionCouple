from random import Random
from ..core.config import Config


class ConfigProvider:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "division": ("STRING", {"default": "1,1"}),
                "orientation": (["horizontal", "vertical"], {"default": "vertical"}),
                "positive": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "negative": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            },
            "optional": {
                "shuffle": ("TILED_SHUFFLE", {"tooltip": "An optional tile shuffle."}),
            },
        }

    CATEGORY = "conditioning"
    FUNCTION = "process"
    RETURN_TYPES = ("TILED_CONFIG",)
    RETURN_NAMES = ("config",)

    def process(self, division, orientation, positive, negative, shuffle=None):
        divisions = [float(x.strip()) for x in division.split(",")]
        positive_base, positive_tiles = self.parse_text(positive, len(divisions))
        negative_base, negative_tiles = self.parse_text(negative, len(divisions))

        if shuffle is not None:
            Random(shuffle).shuffle(positive_tiles)
            Random(shuffle).shuffle(negative_tiles)

        return (
            Config(
                divisions,
                orientation,
                positive_base,
                positive_tiles,
                negative_base,
                negative_tiles,
            ),
        )

    @staticmethod
    def parse_text(value, number_of_divisions):
        parts = [part.strip() for part in value.split("BREAK")]
        tiles = parts[1:] if len(parts) > 1 else []
        tiles = (tiles + [""] * number_of_divisions)[:number_of_divisions]
        return (parts[0], tiles)
