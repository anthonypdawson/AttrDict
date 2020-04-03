"""
A dict that implements MutableAttr.
"""
from attrdict.mixins import MutableAttr

import six


__all__ = ['AttrDict']


class AttrDict(dict, MutableAttr):
    """
    A dict that implements MutableAttr.
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)

        self._setattr('_sequence_type', tuple)
        self._setattr('_allow_invalid_attributes', False)

    def _configuration(self):
        """
        The configuration for an attrmap instance.
        """
        return self._sequence_type

    def __getstate__(self):
        """
        Serialize the object.
        """
        return (
            self.copy(),
            self._sequence_type,
            self._allow_invalid_attributes
        )

    def __setstate__(self, state):
        """
        Deserialize the object.
        """
        mapping, sequence_type, allow_invalid_attributes = state
        self.update(mapping)
        self._setattr('_sequence_type', sequence_type)
        self._setattr('_allow_invalid_attributes', allow_invalid_attributes)

    def __repr__(self):
        return six.u('AttrDict({contents})').format(
            contents=super(AttrDict, self).__repr__()
        )

    def __dir__(self):
        # you may also want to filter the keys to only include the strings
        return sorted(list(super(AttrDict, self).__dir__()) + [k for k in self.keys() if isinstance(k, str)])

    @classmethod
    def _constructor(cls, mapping, configuration):
        """
        A standardized constructor.
        """
        attr = cls(mapping)
        attr._setattr('_sequence_type', configuration)

        return attr
