class AppContainer:

    def __init__(self):
        self._instances = {}

    def register(self, key, value):
        self._instances[key] = value

    def resolve(self, key):
        return self._instances[key]