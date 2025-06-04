from comfy_extras.nodes_mask import MaskComposite, SolidMask
from math import floor
from nodes import CLIPTextEncode, ConditioningSetMask
from .tile import Tile


class Config:
    def __init__(
        self,
        divisions,
        orientation,
        positive_base,
        positive_tiles,
        negative_base,
        negative_tiles,
    ):
        self.divisions = divisions
        self.orientation = orientation
        self.positive_base = positive_base
        self.positive_tiles = positive_tiles
        self.negative_base = negative_base
        self.negative_tiles = negative_tiles

    def process(self, clip, outer, inner):
        mode = "Latent"
        negative_mask = SolidMask().solid(1.0, inner.width, inner.height)[0]
        negative = self.encode(clip, negative_mask, self.negative_base)
        positive_mask = SolidMask().solid(1.0, inner.width, inner.height)[0]
        positive = self.encode(clip, positive_mask, self.positive_base)
        shift = 0

        for i, div in enumerate(self.divisions):
            is_end = i == len(self.divisions) - 1

            if self.orientation == "horizontal":
                base_size = floor(outer.width * (1.0 * div / sum(self.divisions)))
                size = outer.width - shift if is_end else base_size
                tile = Tile(shift, shift + size, 0, outer.height).overlap(inner)
            else:
                base_size = floor(outer.height * (1.0 * div / sum(self.divisions)))
                size = outer.height - shift if is_end else base_size
                tile = Tile(0, outer.width, shift, shift + size).overlap(inner)

            if tile is not None:
                x = tile.x1 - inner.x1
                y = tile.y1 - inner.y1

                base_mask = SolidMask().solid(0.0, inner.width, inner.height)[0]
                tile_mask = SolidMask().solid(1.0, tile.width, tile.height)[0]
                mask = MaskComposite().combine(base_mask, tile_mask, x, y, "add")[0]

                if len(self.positive_tiles) > i:
                    positive += self.encode(clip, mask, self.positive_tiles[i])
                    mode = "Attention"

                if len(self.negative_tiles) > i:
                    negative += self.encode(clip, mask, self.negative_tiles[i])
                    mode = "Attention"

            shift += size

        return (positive, negative, mode)

    @staticmethod
    def encode(clip, mask, text):
        conditioning = CLIPTextEncode().encode(clip, text)[0]
        return ConditioningSetMask().append(conditioning, mask, "default", 1.0)[0]
