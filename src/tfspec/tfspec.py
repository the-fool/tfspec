class Spec:
    def __init__(self, spec):
        self._spec = spec

    @property
    def spec(self):
        return self._spec

    @staticmethod
    def meaning_of_everything():
        return 42

    @staticmethod
    def _is_optional_type(s):
        """Return True if the given key is optional (does not have to be found)"""
        return isinstance(s, Optional)


class Optional(Spec):
    """Marker for an optional part of the validation Schema."""

    _MARKER = object()

    def __init__(self, *args, **kwargs):
        super(Optional, self).__init__(*args, **kwargs)
        self.key = str(self._schema)

    def __hash__(self):
        return hash(self._spec)

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._spec == other._spec
