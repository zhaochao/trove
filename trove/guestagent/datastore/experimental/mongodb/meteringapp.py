# Copyright 2017 Eayun,Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
from trove.guestagent.datastore.service import MeteringApp


class MongoMeteringApp(MeteringApp):
    server_type = 'mongodb'

    def __init__(self, MongoDBAdmin):
        self.MongoDBAdmin = MongoDBAdmin

    def get_counter(self):
        counter = {}
        total = 0

        serverStatus = self.MongoDBAdmin().server_status()
        if serverStatus:
            connections_current = serverStatus['connections']['current']
            connections_available = serverStatus['connections']['available']
            maxConns = int(connections_current) + int(connections_available)
            if maxConns != 0:
                conns_userate = float(connections_current) / float(maxConns)
            else:
                conns_userate = 0
            # insert, query, update, delete, getmore, command, total
            op_mappings = {
                'insert': 'mongo.insert.requests',
                'query': 'mongo.query.requests',
                'update': 'mongo.update.requests',
                'delete': 'mongo.delete.requests',
                'getmore': 'mongo.getmore.requests',
                'command': 'mongo.command.requests'
            }
            for op, status_op in op_mappings.iteritems():
                counter[status_op] = serverStatus['opcounters'][op]
                total += int(serverStatus['opcounters'][op])

            counter.update({'mongo.max.connections': maxConns,
                            'mongo.connections.usage': conns_userate * 100,
                            'mongo.qps': total,
                            'mongo.total.requests': total})

        return counter
