# HammerBotPython
# bug module
# jira_filters.py

"""
This file contains all the necessary jira filters for the proper working of the bug module.
"""

from typing_extensions import Final

fixes_filter: Final[str] = ('project = MC AND '
                            'status = Resolved AND '
                            'resolution = Fixed AND '
                            'resolved >= -1h '
                            'ORDER BY updated DESC')

no_fix_filter: Final[str] = ('project = MC AND '
                             'status = Resolved AND '
                             'resolution = "Won\'t Fix" '
                             'AND resolved >= -1h '
                             'ORDER BY updated DESC')

affected_filter: Final[str] = 'project = MC AND affectedVersion = "{}" ORDER BY updated DESC'

number_fixed_filter: Final[str] = 'project = MC AND fixVersion = "{}" ORDER BY updated DESC'
