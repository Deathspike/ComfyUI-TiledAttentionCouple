class TiledAttentionCoupleConfig:
    def __init__(
        self,
        division,
        orientation,
        positive_base,
        positive_tiles,
        negative_base,
        negative_tiles,
    ):
        self.division = division
        self.orientation = orientation
        self.positive_base = positive_base
        self.positive_tiles = positive_tiles
        self.negative_base = negative_base
        self.negative_tiles = negative_tiles
