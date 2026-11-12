"""Conservative metadata identity rules; these do not fingerprint audio recordings."""
import re
from pathlib import PurePosixPath


def normalized_identity(value):
    value = PurePosixPath(value).stem.lower()
    value = re.sub(r'^mus_c(?:60)?_', '', value)
    value = re.sub(r'^ra_', '', value)
    value = value.replace('darnasssus', 'darnassus').replace('introduction', 'intro')
    value = value.replace('variation', '').replace('walking', 'walk')
    value = re.sub(r'\b0+(\d)', r'\1', value)
    return re.sub(r'[^a-z0-9]', '', value)
