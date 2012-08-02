#!/usr/bin/python

import os
import sys
import logging

from stackutil.novacommand import NovaCommand

class Main(NovaCommand):
    '''Delete volume snapshots from the Nova database.
    
    This command will list (or delete, with ``--purge``) snaphots in states
    other than ``in-use`` or ``available``.  If you pass the ``--all`` flag
    it will operate on all snapshots in the database.'''

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        if args.all:
            res = self.engine.execute('''
                select id,status,display_name from snapshots''')
        else:
            res = self.engine.execute('''
                select id,status,display_name from snapshots
                    where status not in ("in-use", "available")
                        and deleted_at is null''')

        rows = res.fetchall()

        if args.mode == 'purge':
            for id, status, name in rows:
                res = self.engine.execute(
                        'delete from snapshots where id = %s', id)
                self.log.info('deleted snapshot %s (id %s).' % (name, id))

        return(['id', 'status', 'display name'], rows)

