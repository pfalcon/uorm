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

    __pkey__ = "id"

    @classmethod
    def create_table(cls, fail_silently=False):
        c = cls.__db__.conn.cursor()
        try:
            c.execute(cls.__schema__)
        except DB.Error as e:
            if fail_silently:
                print(e)
            else:
                raise
        c.close()

    @classmethod
    def execute(cls, sql, args=()):
        c = cls.__db__.conn.cursor()
        c.execute(sql, args)
        return ResultSet(c)

    @staticmethod
    def render_where(where):
        if where is None:
            return ("1", ())
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
#        s = "INSERT INTO %s(%s) VALUES(%s)" % (
#            cls.__table__, ", ".join(fields.keys()),
#            ", ".join([sqlite3.quote(v) for v in fields.values()])
#        )
        print(s)
        c = cls.__db__.conn.cursor()
        c.execute(s, fields.values())
        c.close()

        if cls.__pkey__ == "id":
            return c.lastrowid

        return list(cls.execute("SELECT %s FROM %s WHERE rowid=%%s" % (cls.__pkey__, cls.__table__), (c.lastrowid,)))[0][0]

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
        print(s, vals + wh_vals)
        c = cls.__db__.conn.cursor()
        c.execute(s, vals + wh_vals)
        c.close()

    @classmethod
    def select(cls, where=None):
        wh_sql, wh_vals = cls.render_where(where)
        s = "SELECT * FROM %s WHERE %s" % (
            cls.__table__,
            wh_sql
        )
        print(s, wh_vals)
        c = cls.__db__.conn.cursor()
        c.execute(s, wh_vals)
        return ResultSet(c)

    @classmethod
    def get_id(cls, id):
        return cls.execute("SELECT * FROM %s WHERE %s=%%s" % (cls.__table__, cls.__pkey__), (id,))
