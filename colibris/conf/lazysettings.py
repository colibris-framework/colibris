
class LazySettings:
    def __init__(self, settings_store, initialize):
        self._settings_store = settings_store
        self._initialized = False
        self._initialize = initialize

    def __getattr__(self, name):
        if not self._initialized:
            self._initialize()
            self._initialized = True

        try:
            return self._settings_store[name]

        except KeyError as e:
            # we want attribute errors instead of key errors on settings
            raise AttributeError(e)
