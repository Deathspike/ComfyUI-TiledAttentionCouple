from .pixel_ksample_hook import PixelKSampleHook

class DetailerHook(PixelKSampleHook):
    def cycle_latent(self, latent):
        return latent

    def post_detection(self, segs):
        return segs

    def post_paste(self, image):
        return image

    def get_custom_noise(self, seed, noise, is_touched):
        return noise, is_touched
