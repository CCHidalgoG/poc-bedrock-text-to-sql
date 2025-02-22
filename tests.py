from chatbackend import query_postgresql
# test de funciones

def test_query_postgres():
    assert query_postgresql("SELECT * FROM users") == [("John", 25), ("Alice", 30)]
