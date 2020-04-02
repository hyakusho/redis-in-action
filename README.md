# redis-in-action

## セットアップ
```
% cp .env.default .env
% docker-compose build
% docker-compose up -d
% docker-compose exec python python src/ch01.py
```

## Redisのコマンド
### STRING
- SET key-name value
- GET key-name
- DEL key-name
```
redis:6379> set hello world
OK
redis:6379> get hello
"world"
redis:6379> del hello
(integer) 1
redis:6379> get hello
(nil)
```
- INCR key-name
- DECR key-name
- INCRBY key-name amount
- DECRBY key-name amount
- INCRYBYFLOAT key-name amount
```
>>> conn = redis.Redis()
>>> conn.get('key')
>>> conn.incr('key')
1
>>> conn.incr('key', 15)
16
>>> conn.decr('key', 5)
11
>>> conn.get('key')
b'11'
>>> conn.set('key', '13')
True
>>> conn.incr('key')
14
```
- APPEND key-name value
- GETRANGE key-name start end
- SETRANGE key-name offset value
- GETBIT key-name offset
- SETBIT key-name offset value
- BITCOUNT key-name [start end]
- BITOP operation dest-key key-name [key-name ...]
```
>>> conn.append('new-string-key', 'hello ')
6
>>> conn.append('new-string-key', 'world!')
12
>>> conn.getrange('new-string-key', 3, 7)
b'lo wo'
>>> conn.setrange('new-string-key', 0, 'H')
12
>>> conn.setrange('new-string-key', 6, 'W')
12
>>> conn.get('new-string-key')
b'Hello World!'
>>> conn.setrange('new-string-key', 11, ', how are you?')
25
>>> conn.get('new-string-key')
b'Hello World, how are you?'
>>> conn.setbit('another-key', 2, 1)
0
>>> conn.setbit('another-key', 7, 1)
0
>>> conn.get('another-key')   # 0x21
b'!'
```
### LIST
- LPUSH/RPUSH key-name value [value ...]
- LPOP/RPOP key-name
- LRANGE key-name start end
- LINDEX offset
```
redis:6379> rpush list-key item
(integer) 1
redis:6379> rpush list-key item2
(integer) 2
redis:6379> rpush list-key item
(integer) 3
redis:6379> lrange list-key 0 -1
1) "item"
2) "item2"
3) "item"
redis:6379> lindex list-key 1
"item2"
redis:6379> lpop list-key
"item"
redis:6379> lrange list-key 0 -1
1) "item2"
2) "item"
```
- LTRIM key-name start end
```
>>> conn.rpush('list-key', 'last')
1
>>> conn.lpush('list-key', 'first')
2
>>> conn.rpush('list-key', 'new last')
3
>>> conn.lrange('list-key', 0, -1)
[b'first', b'last', b'new last']
>>> conn.lpop('list-key')
b'first'
>>> conn.lpop('list-key')
b'last'
>>> conn.lrange('list-key', 0, -1)
[b'new last']
>>> conn.rpush('list-key', 'a', 'b', 'c')
4
>>> conn.lrange('list-key', 0, -1)
[b'new last', b'a', b'b', b'c']
>>> conn.ltrim('list-key', 2, -1)
True
>>> conn.lrange('list-key', 0, -1)
[b'b', b'c']
```
- BLPOP/BRPOP key-name [key-name ...] timeout
- RPOPLPUSH source-key dest-key
- BRPOPLPUSH source-key dest-key timeout
```
>>> conn.rpush('list', 'item1')
1
>>> conn.rpush('list', 'item2')
2
>>> conn.rpush('list2', 'item3')
1
>>> conn.brpoplpush('list2', 'list', 1)
b'item3'
>>> conn.brpoplpush('list2', 'list', 1)
>>> conn.lrange('list', 0, -1)
[b'item3', b'item1', b'item2']
>>> conn.brpoplpush('list', 'list2', 1)
b'item2'
>>> conn.blpop(['list', 'list2'], 1)
(b'list', b'item3')
>>> conn.blpop(['list', 'list2'], 1)
(b'list', b'item1')
>>> conn.blpop(['list', 'list2'], 1)
(b'list2', b'item2')
>>> conn.blpop(['list', 'list2'], 1)
```
### SET
- SADD key-name item [item ...]
- SMEMBERS key-name
- SISMEMBER key-name item
- SREM key-name item [item ...]
```
redis:6379> sadd set-key item
(integer) 1
redis:6379> sadd set-key item2
(integer) 1
redis:6379> sadd set-key item3
(integer) 1
redis:6379> sadd set-key item
(integer) 0
redis:6379> smembers set-key
1) "item2"
2) "item3"
3) "item"
redis:6379> sismember set-key item4
(integer) 0
redis:6379> sismember set-key item
(integer) 1
redis:6379> srem set-key item2
(integer) 1
redis:6379> srem set-key item2
(integer) 0
redis:6379> smembers set-key
1) "item3"
2) "item"
```
- SCARD key-name
- SRANDMEMBER key-name [count]
- SPOP key-name
- SMOVE source-key dest-key item
```
>>> conn.sadd('set-key', 'a', 'b', 'c')
3
>>> conn.srem('set-key', 'c', 'd')
1
>>> conn.srem('set-key', 'c', 'd')
0
>>> conn.scard('set-key')
2
>>> conn.smembers('set-key')
{b'b', b'a'}
>>> conn.smove('set-key', 'set-key2', 'a')
True
>>> conn.smove('set-key', 'set-key2', 'c')
False
>>> conn.smembers('set-key2')
{b'a'}
```
- SDIFF key-name [key-name ...]
- SDIFFSTORE dest-key key-name [key-name ...]
- SINTER key-name [key-name ...]
- SINTERSTORE dest-key key-name [key-name ...]
- SUNION key-name [key-name ...]
- SUNIONSTORE dest-key key-name [key-name ...]
```
>>> conn.sadd('skey1', 'a', 'b', 'c', 'd')
4
>>> conn.sadd('skey2', 'c', 'd', 'e', 'f')
4
>>> conn.sdiff('skey1', 'skey2')
{b'b', b'a'}
>>> conn.sinter('skey1', 'skey2')
{b'c', b'd'}
>>> conn.sunion('skey1', 'skey2')
{b'c', b'b', b'e', b'f', b'a', b'd'}
```
### HASH
- HSET key-name key value
- HGET key-name key
- HGETALL key-name
- HDEL key-name key [key ...]
```
redis:6379> hset hash-key sub-key1 value1
(integer) 1
redis:6379> hset hash-key sub-key2 value2
(integer) 1
redis:6379> hset hash-key sub-key1 value1
(integer) 0
redis:6379> hgetall hash-key
1) "sub-key1"
2) "value1"
3) "sub-key2"
4) "value2"
redis:6379> hdel hash-key sub-key2
(integer) 1
redis:6379> hdel hash-key sub-key2
(integer) 0
redis:6379> hget hash-key sub-key1
"value1"
redis:6379> hgetall hash-key
1) "sub-key1"
2) "value1"
```
- HMGET key-name key [key ...]
- HMSET key-name key value [key value ...]
- HLEN key-name 
```
>>> conn.hmset('hash-key', {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'})
True
>>> conn.hmget('hash-key', ['k2', 'k3'])
[b'v2', b'v3']
>>> conn.hlen('hash-key')
3
>>> conn.hdel('hash-key', 'k1', 'k3')
2
```
- HEXISTS key-name key
- HKEYS key-name
- HVALS key-name
- HINCRBY key-name key increment
- HINCRBYFLOAT key-name key increment
```
>>> conn.hmset('hash-key2', {'short': 'hello', 'long': 1000 * '1'})
True
>>> conn.hkeys('hash-key2')
[b'long', b'short']
>>> conn.hexists('hash-key2', 'num')
False
>>> conn.hincrby('hash-key2', 'num')
1
>>> conn.hexists('hash-key2', 'num')
True
```
### ZSET
- ZADD key-name score member [score member ...]
- ZRANGE key-name start stop [WITHSCORES]
- ZRANGEBYSCORE key-name min max [WITHSCORES] [LIMIT offset count]
- ZREM key-name member [member ...]
```
redis:6379> zadd zset-key 728 member1
(integer) 1
redis:6379> zadd zset-key 982 member0
(integer) 1
redis:6379> zadd zset-key 982 member0
(integer) 0
redis:6379> zrange zset-key 0 -1 withscores
1) "member1"
2) "728"
3) "member0"
4) "982"
redis:6379> zrangebyscore zset-key 0 800 withscores
1) "member1"
2) "728"
redis:6379> zrem zset-key member1
(integer) 1
redis:6379> zrem zset-key member1
(integer) 0
redis:6379> zrange zset-key 0 -1 withscores
1) "member0"
2) "982"
```
- ZCARD key-name
- ZINCRBY key-name increment member
- ZCOUNT key-name min max
- ZRANK key-name member
- ZSCORE key-name member
```
>>> conn.zadd('zset-key', {'a': 3, 'b': 2, 'c': 1})
3
>>> conn.zcard('zset-key')
3
>>> conn.zincrby('zset-key', 3, 'c')
4.0
>>> conn.zscore('zset-key', 'b')
2.0
>>> conn.zcount('zset-key', 0, 3)
2
>>> conn.zrem('zset-key', 'b')
1
>>> conn.zrange('zset-key', 0, -1, withscores=True)
[(b'a', 3.0), (b'c', 4.0)]
```
- ZREVRANK key-name member
- ZREVRANGE key-name start stop [WITHSCORES]
- ZREVRANGEBYSCORE key-name max min [WITHSCORES] [LIMIT offset count]
- ZREMRANGEBYRANK key-name start stop
- ZREMRANGEBYSCORE key-name min max
- ZINTERSTORE dest-key key-count key-name [key-name ...] [WEIGHTS weight [wight ...]] [AGGREGATE SUM|MIN|MAX]
- ZUNIONSTORE dest-key key-count key-name [key-name ...] [WEIGHTS weight [wight ...]] [AGGREGATE SUM|MIN|MAX]
```
>>> conn.zadd('zset-1', {'a': 1, 'b': 2, 'c': 3})
3
>>> conn.zadd('zset-2', {'b': 4, 'c': 1, 'd': 0})
3
>>> conn.zinterstore('zset-i', ['zset-1', 'zset-2'])
2
>>> conn.zrange('zset-i', 0, -1, withscores=True)
[(b'c', 4.0), (b'b', 6.0)]
>>> conn.zunionstore('zset-u', ['zset-1', 'zset-2'], aggregate='min')
4
>>> conn.zrange('zset-u', 0, -1, withscores=True)
[(b'd', 0.0), (b'a', 1.0), (b'c', 1.0), (b'b', 2.0)]
>>> conn.sadd('set-1', 'a', 'd')
2
>>> conn.zunionstore('zset-u2', ['zset-1', 'zset-2', 'set-1'])
4
>>> conn.zrange('zset-u2', 0, -1, withscores=True)
[(b'd', 1.0), (b'a', 2.0), (b'c', 4.0), (b'b', 6.0)]
```
### PUB/SUB
- SUBSCRIBE channel [channel ...]
- UNSUBSCRIBE [channel [channel ...]]
- PUBLISH channel message
- PSUBSCRIBE pattern [pattern ...]
- PUNSUBSCRIBE [pattern [pattern ...]]
```
import redis
import threading
import time

def publisher(n):
    time.sleep(1)
    for i in range(n):
        conn.publish('channel', i)
        time.sleep(1)

def run_pubsub():
    threading.Thread(target=publisher, args=(3,)).start()
    pubsub = conn.pubsub()
    pubsub.subscribe(['channel'])
    count = 0
    for item in pubsub.listen():
        print(item)
        count += 1
        if count == 4:
            pubsub.unsubscribe()
        if count == 5:
            break

if __name__ == '__main__':
    conn = redis.Redis()
    run_pubsub()
```
### ソート
- SORT source-key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC|DESC] [ALPHA] [STORE dest-key]
```
>>> conn.rpush('sort-input', 23, 15, 110, 7)
4
>>> conn.sort('sort-input')
[b'7', b'15', b'23', b'110']
>>> conn.sort('sort-input', alpha=True)
[b'110', b'15', b'23', b'7']
>>> conn.hset('d-7', 'field', 5)
1
>>> conn.hset('d-15', 'field', 1)
1
>>> conn.hset('d-23', 'field', 9)
1
>>> conn.hset('d-110', 'field', 3)
1
>>> conn.sort('sort-input', by='d-*->field')
[b'15', b'110', b'7', b'23']
>>> conn.sort('sort-input', by='d-*->field', get='d-*->field')
[b'1', b'3', b'5', b'9']
```
#### トランザクション
- MULTI/EXEC (pipeline)
```
# no transaction
def notrans():
    print(conn.incr('notrans:'))
    time.sleep(.1)
    conn.incr('notrans:', -1)

if 1:
    for i in range(3):
        threading.Thread(target=notrans).start()
    time.sleep(.5)
```
```
# transaction
def trans():
    pipeline = conn.pipeline()
    pipeline.incr('trans:')
    time.sleep(.1)
    pipeline.incr('trans:', -1)
    print(pipeline.execute()[0])

if 1:
    for i in range(3):
        threading.Thread(target=trans).start()
    time.sleep(.5)
```
### キーの有効期限
- PERSIST key-name
- TTL key-name
- EXPIRE key-name seconds
- EXPIREAT key-name timestamp
- PTTL key-name
- PEXPIRE key-name milliseconds
- PEXPIREAT key-name timestamp-milliseconds
```
>>> conn.set('key', 'value')
True
>>> conn.get('key')
b'value'
>>> conn.expire('key', 2)
True
>>> time.sleep(2)
>>> conn.get('key')
>>> conn.set('key', 'value2')
True
>>> conn.expire('key', 100); conn.ttl('key')
True
100
```
### スナップショット
- BGSAVE
- SAVE
### 追記専用ファイル (AOF)
- BGREWRITEAOF
### レプリケーション (スレーブ側)
- SLAVEOF host port
### 各種情報
- INFO

## データの永続化
### スナップショット
```
# redis.conf
save 60 1000                      # 60秒間に1000回更新があればスナップショットを取る
stop-writes-on-bgsave-error no
rdbcompression yes
dbfilename dump.rdb               # スナップショットのファイル名
```

### 追記専用ファイル (AOF)
```
# redis.conf
appendonly yes                    # 追記専用ファイル有効 (yes|no)
appendfsync everysec              # 同期の頻度 (always|everysync|no)
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100   # BGREWRITEAOFの自動実行を有効にする (前回より100%以上大きくなったら実行)
auto-aof-rewrite-min-size 64mb    # BGREWRITEAOFの自動実行を有効にする (AOFが少なくとも64MBになったら実行)
```

## レプリケーション

## システムエラーの処理
### スナップショットと追記専用ファイルのチェック
```
/data # redis-check-aof
Usage: redis-check-aof [--fix] <file.aof>
/data # redis-check-rdb
Usage: redis-check-rdb <rdb-file-name>
```

## トランザクション
```
/data # redis-benchmark -c 1 -q
```
