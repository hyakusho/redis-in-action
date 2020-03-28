# redis-in-action

## セットアップ
```
% docker-compose build
% docker-compose up -d
% docker-compose exec python python src/ch01.py
```

## Redisのデータ構造
### STRING
- set
- get
- del
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
### LIST
- lpush/rpush
- lpop/rpop
- lrange
- lindex
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
### SET
- sadd
- smembers
- sismember
- srem
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
### HASH
- hset
- hget
- hgetall
- hdel
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
### ZSET
- zadd
- zrange
- zrangebyscore
- zrem
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
