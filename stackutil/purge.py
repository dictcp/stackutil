#!/usr/bin/python

import os
import sys
import logging

from stackutil.nova import NovaCommand

class Purge(NovaCommand):
    '''Clear things from the Nova database.'''

    def take_action(self, args):
        super(Purge, self).take_action(args)
        self.log.info('sql connection: %s' % self.cfg['sql_connection'])

