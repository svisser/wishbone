#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fanout.py
#
#  Copyright 2014 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone import Actor


class Fanout(Actor):

    '''**Forward each incoming message to all connected queues.**

    Forward each incoming message to all connected queues.

    Parameters:

        - name(str)
           |  The name of the module.

        - size(int)
           |  The default max length of each queue.

        - frequency(int)
           |  The frequency in seconds to generate metrics.


    Queues:

        outbox
         |  Outgoing events.

    '''

    def __init__(self, name, size=100, frequency=1):

        Actor.__init__(self, name, size, frequency)
        self.name = name
        self.pool.createQueue("outbox")

    def preHook(self):

        for queue in self.pool.listQueues(name=True, default=False):
            if queue != "outbox":
                self.registerConsumer(self.consume, queue)

    def consume(self, event):

        self.submit(event, self.pool.queue.outbox)
