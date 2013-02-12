def invalidate(model):
    try:  # try invalidating cache for model (have no idea if this is right)
        from johnny.cache import invalidate
        invalidate(model)
    except:
        pass
