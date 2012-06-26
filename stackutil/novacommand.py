#!/usr/bin/python

import logging

from cliff.command import Command

from sqlalchemy.engine import create_engine

from nova import flags
from nova import service
from nova import utils

class NovaCommand (Command):
    '''Base class for commands that interact with the Nova database.'''

    log = logging.getLogger(__name__)
    
    def get_parser (self, *args, **kwargs):
        p = super(NovaCommand, self).get_parser(*args, **kwargs)
        p.add_argument('-f', '--flagfile', default='/etc/nova/nova.conf')
        p.add_argument('-n', '--dryrun', action='store_true')
        return p

    def take_action(self, args):
        flags.FLAGS(['', '--flagfile=%s' % args.flagfile])
        self.cfg = flags.FLAGS
        self.log.debug('using sql_connection: %s' %
                (self.cfg['sql_connection']))
        self.engine = create_engine(self.cfg['sql_connection'])

        # This tests the connection and should raise an exception
        # if it fails.
        self.engine.execute('select 1')

