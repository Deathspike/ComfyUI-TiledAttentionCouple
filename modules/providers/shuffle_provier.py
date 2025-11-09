MAX = 0xFFFFFFFFFFFFFFFF


class ShuffleProvider:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"control_after_generate": True, "min": 0, "max": MAX}),
            }
        }

    CATEGORY = "conditioning"
    FUNCTION = "process"
    RETURN_TYPES = ("TILED_SHUFFLE",)
    RETURN_NAMES = ("shuffle",)

    def process(self, seed):
        return (seed,)
