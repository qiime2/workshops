# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

"""
Testing env (e.g. travis ci) settings
"""

from .local import * # gross but is the best for now


DATABASES['default'] = env.db("DATABASE_URL")
