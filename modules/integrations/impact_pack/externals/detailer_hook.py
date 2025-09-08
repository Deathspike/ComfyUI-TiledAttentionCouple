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

    def get_custom_sampler(self):
        return None

    def get_skip_sampling(self):
        return False

    def should_retry_patch(self, patch):
        return False
