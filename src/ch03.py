import redis
import threading
import time
import unittest

ARTICLES_PER_PAGE =25
ONE_WEEK_IN_SECONDS = 7 * 86400
THIRTY_DAYS = 30 * 86400
VOTE_SCORE = 432

def article_vote(conn, user, article):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    posted = conn.zscore('time:', article)
    if posted < cutoff:
        return

    article_id = article.partition(':')[-1]
    pipeline = conn.pipeline()
    pipeline.sadd('voted:' + article_id, user)
    pipeline.expire('voted:' + article_id, int(posted - cutoff))
    if pipeline.execute()[0]:
        pipeline.zincrby('score:',VOTE_SCORE, article)
        pipeline.hincrby(article, 'votes', 1)
        pipeline.execute()

def post_article(conn, user, title, link):
    article_id = str(conn.incr('article:'))

    voted = 'voted:' + article_id
    conn.sadd(voted, user)
    conn.expire(voted, ONE_WEEK_IN_SECONDS)

    now = time.time()
    article = 'article:' + article_id
    conn.hmset(article, {
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1,
    })

    conn.zadd('score:', {article: now + VOTE_SCORE})
    conn.zadd('time:', {article: now})

    return article_id

def get_articles(conn, page, order='score:'):
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    ids = conn.zrevrange(order, start, end)

    pipeline = conn.pipeline()
    all(map(pipeline.hgetall, ids))

    articles = []
    for id, article_data in zip(ids, pipeline.execute()):
        article_data['id'] = id
        articles.append(article_data)

    return articles

def check_token(conn, token):
    return conn.get('login:' + token)

def update_token(conn, token, user, item=None):
    conn.setex('login:' + token, user, THIRTY_DAYS)
    key = 'viewed:' + token
    if item:
        conn.lrem(key, item)
        conn.rpush(key, item)
        conn.ltrim(key, -25, -1)
        conn.zincrby('viewed:', -1, item)
    conn.expire(key, THIRTY_DAYS)

def add_to_cart(conn, session, item, count):
    key = 'cart:' + session
    if count <= 0:
        conn.hrem(key, item)
    else:
        conn.hset(key, item, count)
    conn.expire(key, THIRTY_DAYS)
