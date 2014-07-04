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

    # Example of custom query method
    @classmethod
    def public(cls):
        return cls.execute("""
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
    # Get row by id
    print("get_id", list(Note.get_id(1)))
    # Get using select method
    print("select", list(Note.select({"timestamp": "20140609"})))
    # Get using custom query method
    print("custom", list(Note.public()))
    db.close()
