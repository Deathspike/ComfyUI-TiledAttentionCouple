class PixelKSampleHook:
    def set_steps(self, info):
        pass

    def post_decode(self, pixels):
        return pixels

    def post_upscale(self, pixels):
        return pixels

    def post_encode(self, samples):
        return samples

    def pre_decode(self, samples):
        return samples

    def pre_ksample(self, *args):
        return args

    def post_crop_region(self, w, h, item_bbox, crop_region):
        return crop_region

    def touch_scaled_size(self, w, h):
        return w, h
