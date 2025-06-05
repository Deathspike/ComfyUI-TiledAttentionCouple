from nodes import MAX_RESOLUTION
from ..attention_couple import AttentionCouple
from ..core.funcs import get_latent_size
from ..core.tile import Tile


class TiledProvider:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "config": ("TILED_CONFIG",),
                "width": ("INT", {"default": 512, "min": 0, "max": MAX_RESOLUTION}),
                "height": ("INT", {"default": 512, "min": 0, "max": MAX_RESOLUTION}),
            }
        }

    CATEGORY = "conditioning"
    FUNCTION = "process"
    RETURN_TYPES = ("MODEL", "CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("model", "positive", "negative")

    def process(self, model, clip, config, width, height):
        self.validate(model, width, height)
        tile = Tile(0, 0, width, height)
        positive, negative, mode = config.process(clip, tile, tile)
        return AttentionCouple().attention_couple(model, positive, negative, mode)

    @staticmethod
    def validate(model, width, height):
        latent_size = get_latent_size(model)
        if width % latent_size != 0:
            raise ValueError(f"Width must be divisible by {latent_size}.")
        if height % latent_size != 0:
            raise ValueError(f"Height must be divisible by {latent_size}.")
