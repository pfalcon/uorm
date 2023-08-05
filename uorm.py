import sqlite3


class DB:

    Error = sqlite3.Error

    def __init__(self, name):
        self.name = name

    def connect(self):
        self.conn = sqlite3.connect(self.name)

    def close(self):
        self.conn.close()


class ResultSet:

    def __init__(self, c):
        self.c = c

    def __iter__(self):
        return self

    def __next__(self):
        row = self.c.fetchone()
        if row is None:
            self.c.close()
            raise StopIteration
        return row


class Model:

    @classmethod
    def create_table(cls):
        c = cls.__db__.conn.cursor()
        try:
            c.execute(cls.__schema__)
        except DB.Error as e:
            print(e)
        c.close()

    @staticmethod
    def render_where(where):
        if isinstance(where, int):
            return ("id=%s",  (where,))
        if isinstance(where, dict):
            keys = []
            vals = []
            for k, v in where.items():
                keys.append("%s=%%s" % k)
                vals.append(v)
            return (" AND ".join(keys), vals)
        return (where, ())

    @classmethod
    def create(cls, **fields):
        s = "INSERT INTO %s(%s) VALUES(%s)" % (
            cls.__table__, ", ".join(fields.keys()),
            ", ".join(["%s"] * len(fields))
        )
        c = cls.__db__.conn.cursor()
        c.execute(s, fields.values())
        c.close()
        return c.lastrowid

    @classmethod
    def update(cls, where, **fields):
        keys = []
        vals = []
        for k, v in fields.items():
            keys.append("%s=%%s" % k)
            vals.append(v)

        wh_sql, wh_vals = cls.render_where(where)
        s = "UPDATE %s SET %s WHERE %s" % (
            cls.__table__, ", ".join(keys),
            wh_sql
        )
        c = cls.__db__.conn.cursor()
        c.execute(s, vals + wh_vals)
        c.close()

    @classmethod
    def select(cls, sql, args=()):
        c = cls.__db__.conn.cursor()
        c.execute(sql, args)
        return ResultSet(c)

    @classmethod
    def get_id(cls, id):
        return cls.select("SELECT * FROM %s WHERE id=%%s" % cls.__table__, (id,))
