#!/usr/bin/python

import logging

from cliff.command import Command
from cliff.lister import Lister

from sqlalchemy.engine import create_engine

from nova import flags
from nova import service
from nova import utils

class NovaCommand (Lister):
    '''Base class for commands that interact with the Nova database.'''

    log = logging.getLogger(__name__)
    
    def get_parser (self, *args, **kwargs):
        p = super(NovaCommand, self).get_parser(*args, **kwargs)

        g = p.add_argument_group('Gemeral options')
        g.add_argument('--flagfile', default='/etc/nova/nova.conf',
                help='Path to Nova configuration file.')
        g.add_argument('--purge', action='store_const', dest='mode',
                const='purge',
                help='Delete or otherwise clear entries in the database.')
        g.add_argument('--list', action='store_const', dest='mode',
                const='list',
                help='List entries in the database (this is the default behavior')
        g.add_argument('--all', action='store_true',
                help='Show all entries')
        g.add_argument('--id',
                help='Operate on a particular entity.')

        p.set_defaults(mode='list')

        return p

    def init_engine(self, args):
        flags.FLAGS(['', '--flagfile=%s' % args.flagfile])
        self.cfg = flags.FLAGS
        self.log.debug('using sql_connection: %s' %
                (self.cfg['sql_connection']))
        self.engine = create_engine(self.cfg['sql_connection'])

        # This tests the connection and should raise an exception
        # if it fails.
        self.engine.execute('select 1')

