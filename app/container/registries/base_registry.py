class Registory:
    
    def __init__(self, providers: dict):
        self._providers = {
            name: provider()
            for name, provider in providers.items()
        }

    def get(self, name):

        try:
            return self._providers[name]
        except KeyError:
            raise ValueError(f"Unknown provider '{name}'")
