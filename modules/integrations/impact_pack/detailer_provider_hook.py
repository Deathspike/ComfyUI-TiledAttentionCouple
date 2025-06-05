from ...attention_couple import AttentionCouple
from ...core.tile import Tile
from .externals.detailer_hook import DetailerHook


class DetailerProviderHook(DetailerHook):
    def __init__(self, latent_size, clip, config):
        self.latent_size = latent_size
        self.clip = clip
        self.config = config

    def post_crop_region(self, w, h, item_bbox, crop_region):
        x1, y1, x2, y2 = crop_region
        x2 -= (x2 - x1) % self.latent_size
        y2 -= (y2 - y1) % self.latent_size
        return [x1, y1, x2, y2]

    def post_detection(self, segs):
        shape, items = segs
        self.regions = [item.crop_region for item in items]
        self.shape = shape
        return segs

    def pre_ksample(
        self,
        model,
        seed,
        steps,
        cfg,
        sampler_name,
        scheduler,
        positive,
        negative,
        latent_image,
        denoise,
    ):
        x1, y1, x2, y2 = self.regions.pop(0)
        outer = Tile(0, self.shape[1], 0, self.shape[0])
        inner = Tile(x1, x2, y1, y2)

        model, positive, negative = AttentionCouple().attention_couple(
            model, *self.config.process(self.clip, outer, inner)
        )

        return (
            model,
            seed,
            steps,
            cfg,
            sampler_name,
            scheduler,
            positive,
            negative,
            latent_image,
            denoise,
        )

    def touch_scaled_size(self, w, h):
        w -= w % self.latent_size
        h -= h % self.latent_size
        return w, h
