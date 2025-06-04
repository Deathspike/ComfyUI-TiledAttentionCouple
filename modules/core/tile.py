class Tile:
    def __init__(self, x1, x2, y1, y2):
        self.height = y2 - y1
        self.width = x2 - x1
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def overlap(self, inner):
        x1 = max(self.x1, inner.x1)
        y1 = max(self.y1, inner.y1)
        x2 = min(self.x2, inner.x2)
        y2 = min(self.y2, inner.y2)
        return Tile(x1, x2, y1, y2) if x1 < x2 and y1 < y2 else None
