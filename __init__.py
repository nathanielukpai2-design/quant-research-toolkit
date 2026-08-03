"""Repository-wide configuration, per Engineering Manual §7.

`constants.py` holds fixed, non-tunable definitions. `defaults.py`
holds tunable default parameters that callers may override. Business
logic modules import from here rather than defining their own
literals, so a given value is defined in exactly one place.
"""
