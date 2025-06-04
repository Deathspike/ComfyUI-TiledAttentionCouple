from .detailer_provider_hook import DetailerProviderHook


class DetailerProvider:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "config": ("TILED_CONFIG",),
            }
        }

    CATEGORY = "conditioning"
    FUNCTION = "process"
    RETURN_TYPES = ("DETAILER_HOOK",)
    RETURN_NAMES = ("detailer_hook",)

    def process(self, model, clip, config):
        return (DetailerProviderHook(model, clip, config),)
