from django.conf import settings

from redis.client import Redis


class Statistics:
    CON = Redis(
        host=settings.REDIS_STATISTICS_HOST, port=settings.REDIS_STATISTICS_PORT,
        db=settings.REDIS_STATISTICS_DB, decode_responses=True,
    )

    def __init__(self, product_id):
        self.con = self.CON
        self.product_id = product_id

    @property
    def key(self):
        return f'flow_{self.product_id}'

    @property
    def key_uv_add(self):
        return f'flow_uv_{self.product_id}'

    def add_uv(self, info):
        identify = info['identify']
        meta = info['meta']

        key = self.key_uv_add
        root_key = self.key

        def func(pipe):
            if identify and pipe.sismember(key, identify):
                return

            ip = meta.get('HTTP_X_FORWARDED_FOR') or meta.get('REMOTE_ADDR')
            if not ip:
                return
            if pipe.sismember(key, ip):
                return

            pipe.multi()
            if identify:
                pipe.sadd(key, identify)
            pipe.sadd(key, ip)
            pipe.incr(root_key, 1)
            return 'success'

        return self.con.transaction(func, key, value_from_callable=True)

    def get_uv_num(self):
        n = self.con.get(self.key)
        n = n and int(n) or 0
        return n
