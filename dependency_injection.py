class DependencyContainer:
    def __init__(self):
        self._dependencies = {}

    def register(self, key, dependency):
        self._dependencies[key] = dependency

    def get(self, key):
        if key not in self._dependencies:
            raise KeyError(f"No such dependency registered: {key}")
        return self._dependencies[key]

container = DependencyContainer()
