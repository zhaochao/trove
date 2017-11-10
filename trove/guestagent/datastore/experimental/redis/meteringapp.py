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


from trove.guestagent.datastore.experimental.redis.commandstat \
    import commandstats
from trove.guestagent.datastore.service import MeteringApp

REDIS_DB_NUMBER = 16


class RedisMeteringApp(MeteringApp):
    server_type = 'redis'

    def __init__(self, client):
        self.__client = client

    def set_client(self, client):
        self.__client = client

    def countcommands(self, cmd_stat_list, info):
        qps = 0
        for key in cmd_stat_list:
            if key in info:
                qps += int(info[key]['calls'])
        return qps

    def countkeys(self, info):
        keys = 0
        for i in range(REDIS_DB_NUMBER):
            dbname = 'db' + str(i)
            if dbname in info:
                keys += int(info[dbname]['keys'])
        return keys

    def get_counter(self):
        counter = {}
        info = self.__client.get_info(section='all')

        used_memory_rss = info['used_memory_rss']
        total_system_memory = info['total_system_memory']
        if float(total_system_memory) != 0:
            memory_userate = float(used_memory_rss) / \
                float(total_system_memory)
        else:
            memory_userate = 0

        qps = info['total_commands_processed']

        total_connections_received = info['total_connections_received']

        keys = self.countkeys(info)

        connected_clients = info['connected_clients']

        expired_keys = info['expired_keys']

        evicted_keys = info['evicted_keys']

        keyspace_hits = info['keyspace_hits']

        keyspace_misses = info['keyspace_misses']
        keyspace = float(keyspace_hits) + float(keyspace_misses)
        if keyspace != 0:
            keyspace_hits_rate = float(keyspace_hits) / keyspace
        else:
            keyspace_hits_rate = 0

        setQPS = self.countcommands(commandstats['set'], info)

        listQPS = self.countcommands(commandstats['list'], info)

        stringQPS = self.countcommands(commandstats['string'], info)

        hashQPS = self.countcommands(commandstats['hash'], info)

        zsetQPS = self.countcommands(commandstats['zset'], info)

        hyperloglogQPS = self.countcommands(commandstats['hyperloglog'], info)

        pubsubQPS = self.countcommands(commandstats['pubsub'], info)

        transactionQPS = self.countcommands(commandstats['transaction'], info)

        counter.update({'redis.memory.usage': memory_userate * 100,
                        'redis.qps': qps,
                        'redis.total.received.connections':
                        total_connections_received,
                        'redis.clients.connections': connected_clients,
                        'redis.total.keys': keys,
                        'redis.expire.keys': expired_keys,
                        'redis.evicte.keys': evicted_keys,
                        'redis.keyspace.hits': keyspace_hits,
                        'redis.keyspace.hits.ratio': keyspace_hits_rate * 100,
                        'redis.set.qps': setQPS,
                        'redis.list.qps': listQPS,
                        'redis.string.qps': stringQPS,
                        'redis.hash.qps': hashQPS,
                        'redis.zset.qps': zsetQPS,
                        'redis.hyperloglog.qps': hyperloglogQPS,
                        'redis.pubsub.qps': pubsubQPS,
                        'redis.transaction.qps': transactionQPS})

        return counter
