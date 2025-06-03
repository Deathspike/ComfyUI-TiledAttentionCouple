def get_latent_size(model):
    if hasattr(model.model.diffusion_model, "label_emb"):
        return 64
    else:
        return 32
