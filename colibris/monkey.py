
# Patch marshmallow to provide marshmallow.compat.string_types,
# so that marshmallow-peewee<=2.2.0 can be used.
# This can be removed as soon as the following PR gets merged:
# https://github.com/klen/marshmallow-peewee/pull/61/commits/462b78aea70ff818ab501be2d3d2cead420c274e

import marshmallow.compat
marshmallow.compat.string_types = (str,)
