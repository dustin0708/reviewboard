"""Diff viewer model mixins."""

from __future__ import unicode_literals

import collections

from django.db import models
from django.utils import six
from djblets.db.fields import RelationCounterField


class FileDiffCollectionMixin(models.Model):
    """A mixin for models that consist of a colleciton of FileDiffs."""

    file_count = RelationCounterField('files')

    def get_total_line_counts(self):
        """Return the total line counts of all child FileDiffs.

        Returns:
            dict:
            A dictionary with the following keys:

            * ``raw_insert_count``
            * ``raw_delete_count``
            * ``insert_count``
            * ``delete_count``
            * ``replace_count``
            * ``equal_count``
            * ``total_line_count``

            Each entry maps to the sum of that line count type for all child
            :py:class:`FileDiffs
            <reviewboard.diffviewer.models.filediff.FileDiff>`.
        """
        counts = {
            'raw_insert_count': 0,
            'raw_delete_count': 0,
            'insert_count': 0,
            'delete_count': 0,
            'replace_count': None,
            'equal_count': None,
            'total_line_count': None,
        }

        for filediff in self.files.all():
            for key, value in six.iteritems(filediff.get_line_counts()):
                if value is not None:
                    if counts[key] is None:
                        counts[key] = value
                    else:
                        counts[key] += value

        return dict(counts)

    class Meta:
        abstract = True
