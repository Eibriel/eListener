try:
    from elistener.config.local import Local as Config
except:
    print("Loading default Config")
    from elistener.config.default import Config
