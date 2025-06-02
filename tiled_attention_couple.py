from comfy_extras.nodes_mask import MaskComposite, SolidMask
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
    RETURN_NAMES = ("model", "positive", "negative")

    def process(self, model, clip, config, width, height):
        self.validate(model, width, height)
        negative_mask = SolidMask().solid(1.0, width, height)[0]
        negative = self.encode(clip, negative_mask, config.negative_base)
        positive_mask = SolidMask().solid(1.0, width, height)[0]
        positive = self.encode(clip, positive_mask, config.positive_base)
        requiresAttention = False
        shift = 0

        for i, division in enumerate(config.divisions):
            is_last = i == len(config.divisions) - 1
            main = SolidMask().solid(0.0, width, height)[0]

            if config.orientation == "horizontal":
                tile_size = width - shift if is_last else config.size(division, width)
                tile_mask = SolidMask().solid(1.0, tile_size, height)[0]
                tile_mask = MaskComposite().combine(main, tile_mask, shift, 0, "add")[0]
                shift += tile_size
            else:
                tile_size = height - shift if is_last else config.size(division, height)
                tile_mask = SolidMask().solid(1.0, width, tile_size)[0]
                tile_mask = MaskComposite().combine(main, tile_mask, 0, shift, "add")[0]
                shift += tile_size

            if len(config.positive_tiles) > i:
                positive += self.encode(clip, tile_mask, config.positive_tiles[i])
                requiresAttention = True

            if len(config.negative_tiles) > i:
                negative += self.encode(clip, tile_mask, config.negative_tiles[i])
                requiresAttention = True

        if requiresAttention:
            return AttentionCouple().attention_couple(
                model, positive, negative, "Attention"
            )

        return (model, positive, negative)

    @staticmethod
    def encode(clip, mask, text):
        conditioning = CLIPTextEncode().encode(clip, text)[0]
        return ConditioningSetMask().append(conditioning, mask, "default", 1.0)[0]

    @staticmethod
    def validate(model, width, height):
        if hasattr(model.model.diffusion_model, "label_emb"):
            if width % 64 != 0 or height % 64 != 0:
                raise ValueError(f"Width and height must be divisible by 64.")
        else:
            if width % 32 != 0 or height % 32 != 0:
                raise ValueError(f"Width and height must be divisible by 32.")
