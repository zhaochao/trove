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


class MysqlMeteringApp(MeteringApp):
    server_type = 'mysql'

    def __init__(self, mysql_admin):
        self.mysql_admin = mysql_admin

    def get_counter(self):
        mysql_variables = self.mysql_admin().get_mysql_variables()
        mysql_status = self.mysql_admin().get_mysql_status()
        slave_status = self.mysql_admin().get_slave_status()

        max_connections = mysql_variables.get('max_connections')

        innodb_buffer_pool_size = \
            mysql_variables.get('innodb_buffer_pool_size')
        innodb_buffer_pool_size = float(innodb_buffer_pool_size) / 1024 / 1024

        connections = mysql_status.get('Connections')

        threads_connected = mysql_status.get('Threads_connected')

        qps = mysql_status.get('Queries')

        com_commit = mysql_status.get('Com_commit')

        com_rollback = mysql_status.get('Com_rollback')

        tps = int(com_commit) + int(com_rollback)

        slow_queries = mysql_status.get('Slow_queries')

        handler_read_rnd_next = mysql_status.get('Handler_read_rnd_next')

        innodb_buffer_pool_pages_dirty = \
            mysql_status.get('Innodb_buffer_pool_pages_dirty')
        innodb_buffer_pool_pages_data = \
            mysql_status.get('Innodb_buffer_pool_pages_data')
        if float(innodb_buffer_pool_pages_data) != 0:
            innodb_buffer_pool_userate = \
                float(innodb_buffer_pool_pages_dirty) / \
                float(innodb_buffer_pool_pages_data)
        else:
            innodb_buffer_pool_userate = 0

        Innodb_buffer_pool_reads = mysql_status.get('Innodb_buffer_pool_reads')
        Innodb_buffer_pool_read_requests = \
            mysql_status.get('Innodb_buffer_pool_read_requests')
        if float(Innodb_buffer_pool_read_requests) != 0:
            innodb_buffer_pool_reads_hitrate = \
                float(Innodb_buffer_pool_reads) / \
                float(Innodb_buffer_pool_read_requests)
        else:
            innodb_buffer_pool_reads_hitrate = 0

        qcahce_hits = mysql_status.get('Qcahce_hits', 0)
        qcache_inserts = mysql_status.get('Qcache_inserts', 0)
        qcahce = float(qcahce_hits) + float(qcache_inserts)
        if qcahce != 0:
            qcache_hits_rate = float(qcahce_hits) / qcahce
        else:
            qcache_hits_rate = 0

        threads_created = mysql_status.get('Threads_created')
        if float(connections) != 0:
            thread_cache_hitrate = 1 - float(
                threads_created) / float(connections)
        else:
            thread_cache_hitrate = 0

        threads_running = mysql_status.get('Threads_running')

        com_select = mysql_status.get('Com_select')

        replaceQPS = mysql_status.get('Com_replace')

        seconds_Behind_Master = slave_status.get('Seconds_Behind_Master', 0)

        counter = {'mysql.total.connections': int(connections),
                   'mysql.threads.connections': int(threads_connected),
                   'mysql.qps': int(qps),
                   'mysql.tps': tps,
                   'mysql.slow.querys': int(slow_queries),
                   'mysql.sync.delay': int(seconds_Behind_Master),
                   'mysql.scan.full.table': int(handler_read_rnd_next),
                   'mysql.buffer.pool.dirty.ratio':
                   innodb_buffer_pool_userate * 100,
                   'mysql.buffer.pool.size': int(innodb_buffer_pool_size),
                   'mysql.buffer.pool.read.hits.ratio':
                   innodb_buffer_pool_reads_hitrate * 100,
                   'mysql.qcahce.query.hits.ratio': qcache_hits_rate * 100,
                   'mysql.cached.connections.hits.ratio':
                   thread_cache_hitrate * 100,
                   'mysql.threads.running': int(threads_running),
                   'mysql.max.connections': int(max_connections),
                   'mysql.transaction.commit': int(com_commit),
                   'mysql.transaction.rollback': int(com_rollback),
                   'mysql.total.select': int(com_select),
                   'mysql.replace.qps': int(replaceQPS)}

        return counter
