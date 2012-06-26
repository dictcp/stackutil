#!/usr/bin/python

import logging

from cliff.command import Command

from  sqlalchemy import engine

from nova import flags
from nova import service
from nova import utils

class NovaCommand (Command):
    '''Base class for commands that interact with the Nova database.'''

    log = logging.getLogger(__name__)
    
    def get_parser (*args, **kwargs):
        p = super(NovaCommand, self).get_parser(*args, **kwargs)
        p.add_argument('-f', '--flagfile', default='/etc/nova/nova.conf')
        return p

    def take_action(self, args):
        flags.FLAGS(['', '--flagfile=%s' % args.flagfile])
        self.cfg = flags.FLAGS

