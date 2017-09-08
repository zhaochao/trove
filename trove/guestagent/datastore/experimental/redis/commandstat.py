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


commandstats = {
    'set': [
        'cmdstat_sadd',
        'cmdstat_acard',
        'cmdstat_sdiff',
        'cmdstat_sdiffstore',
        'cmdstat_sinter',
        'cmdstat_sinterstore',
        'cmdstat_sismember',
        'cmdstat_smembers',
        'cmdstat_smove',
        'cmdstat_spop',
        'cmdstat_srandmember',
        'cmdstat_srem',
        'cmdstat_sunion',
        'cmdstat_sunionstore',
        'cmdstat_sscan'
        ],
    'list': [
        'cmdstat_blpop',
        'cmdstat_brpop',
        'cmdstat_brpoplpush',
        'cmdstat_lindex',
        'cmdstat_linsert',
        'cmdstat_llen',
        'cmdstat_lpop',
        'cmdstat_lpush',
        'cmdstat_lpushx',
        'cmdstat_lrange',
        'cmdstat_lrem',
        'cmdstat_lset',
        'cmdstat_ltrim',
        'cmdstat_rpop',
        'cmdstat_rpoplpush',
        'cmdstat_rpush',
        'cmdstat_rpushx'
        ],
    'string': [
        'cmdstat_append',
        'cmdstat_bitcount',
        'cmdstat_bitop',
        'cmdstat_decr',
        'cmdstat_decrby',
        'cmdstat_get',
        'cmdstat_getbit',
        'cmdstat_getrange',
        'cmdstat_getset',
        'cmdstat_incr',
        'cmdstat_incrby',
        'cmdstat_incrbyfloat',
        'cmdstat_mget',
        'cmdstat_mset',
        'cmdstat_msetnx',
        'cmdstat_psetex',
        'cmdstat_set',
        'cmdstat_setbit',
        'cmdstat_setex',
        'cmdstat_setnx',
        'cmdstat_setrange',
        'cmdstat_strlen'
        ],
    'hash': [
        'cmdstat_hdel',
        'cmdstat_hexists',
        'cmdstat_hget',
        'cmdstat_hgetall',
        'cmdstat_hincrby',
        'cmdstat_hincrbyfloat',
        'cmdstat_hkeys',
        'cmdstat_hlen',
        'cmdstat_hmget',
        'cmdstat_hmset',
        'cmdstat_hset',
        'cmdstat_hsetnx',
        'cmdstat_hvals',
        'cmdstat_hscan'
        ],
    'zset': [
        'cmdstat_zadd',
        'cmdstat_zcard',
        'cmdstat_zcount',
        'cmdstat_zincrby',
        'cmdstat_zrange',
        'cmdstat_zrangebyscore',
        'cmdstat_zrank',
        'cmdstat_zrem',
        'cmdstat_zremrangebyrank',
        'cmdstat_zremrangebyscore',
        'cmdstat_zrevrange',
        'cmdstat_zrevrangebyscore',
        'cmdstat_zrevrank',
        'cmdstat_zscore',
        'cmdstat_zunionstore',
        'cmdstat_zinterstore',
        'cmdstat_zscan'
        ],
    'hyperloglog': [
        'cmdstat_pfadd',
        'cmdstat_pfcount',
        'cmdstat_pfmerge'
        ],
    'pubsub': [
        'cmdstat_psubscribe',
        'cmdstat_publish',
        'cmdstat_pubsub',
        'cmdstat_punsubscribe',
        'cmdstat_subscribe',
        'cmdstat_unsubscribe'
        ],
    'transaction': [
        'cmdstat_discard',
        'cmdstat_exec',
        'cmdstat_multi',
        'cmdstat_unwatch',
        'cmdstat_watch'
        ]
}
