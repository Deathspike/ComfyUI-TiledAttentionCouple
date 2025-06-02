from math import floor


class TiledAttentionCoupleConfig:
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

    def size(self, division, total):
        return floor(total * (1.0 * division / sum(self.divisions)))
