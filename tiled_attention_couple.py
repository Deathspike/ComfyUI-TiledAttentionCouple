from comfy_extras.nodes_mask import MaskComposite, SolidMask
from math import floor
from nodes import CLIPTextEncode, ConditioningSetMask, MAX_RESOLUTION
from .attention_couple import AttentionCouple


class TiledAttentionCouple:
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

    def process(self, model, clip, config, width, height):
        division_sum = sum(config.division)
        negative_mask = SolidMask().solid(1.0, width, height)[0]
        negative = encode_with_mask(clip, negative_mask, config.negative_base)
        positive_mask = SolidMask().solid(1.0, width, height)[0]
        positive = encode_with_mask(clip, positive_mask, config.positive_base)
        requiresAttention = False
        shift = 0

        for i, division in enumerate(config.division):
            main = SolidMask().solid(0.0, width, height)[0]

            if config.orientation == "horizontal":
                tile_width = floor(width * (1.0 * division / division_sum))
                tile_mask = SolidMask().solid(1.0, tile_width, height)[0]
                tile_mask = MaskComposite().combine(main, tile_mask, shift, 0, "add")[0]
                shift += tile_width
            else:
                tile_height = floor(height * (1.0 * division / division_sum))
                tile_mask = SolidMask().solid(1.0, width, tile_height)[0]
                tile_mask = MaskComposite().combine(main, tile_mask, 0, shift, "add")[0]
                shift += tile_height

            if len(config.positive_tiles) > i:
                positive += encode_with_mask(clip, tile_mask, config.positive_tiles[i])
                requiresAttention = True

            if len(config.negative_tiles) > i:
                negative += encode_with_mask(clip, tile_mask, config.negative_tiles[i])
                requiresAttention = True

        if requiresAttention:
            return AttentionCouple().attention_couple(
                model, positive, negative, "Attention"
            )
        
        return (model, positive, negative)


def encode_with_mask(clip, mask, text):
    return ConditioningSetMask().append(
        CLIPTextEncode().encode(clip, text)[0],
        mask,
        "default",
        1.0,
    )[0]
