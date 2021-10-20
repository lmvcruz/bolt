class Parameter(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, d={}) -> None:
        super().__init__(d)

    def add_attribute(self, name: str, val) -> None:
        setattr(self, name, val)
