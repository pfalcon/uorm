import uorm


# Instantiate DB object to reference from models.
# Note that this just creates object for a named database,
# not opens DB file/connection.
db = uorm.DB("example.db")


class Note(uorm.Model):

    __db__ = db
    __table__ = "note"
    # __schema__ will be used to create a table
    __schema__ = """
        CREATE TABLE note(
        id INTEGER PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        archived INT NOT NULL DEFAULT 0,
        content TEXT NOT NULL
        )
    """

    # Example of query method
    @classmethod
    def public(cls):
        return cls.select("""
            SELECT * FROM note
            WHERE archived=0
            ORDER BY timestamp
        """)


if __name__ == "__main__":
    db.connect()
    Note.create_table()
    Note.create(content="foo")
    Note.create(timestamp="20140609", content="foo")
    Note.update(where={"timestamp": "20140609"}, content="foo bar")
    print(list(Note.public()))
    print(list(Note.get_id(1)))
    db.close()
