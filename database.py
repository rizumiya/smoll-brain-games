import sqlite3
import psycopg2


class Database:
    def __init__(self, postgresql_url: str = None, sqlite_path: str = None):
        self.postgresql_url = postgresql_url
        self.sqlite_path = sqlite_path
        self.query = None
        self.values = None

    def set_query(self, query, values=None):
        """Menetapkan query dan nilai-nilai yang akan digunakan."""
        self.query = query
        self.values = values

    def execute_query(self, commit=True):
        """Mengeksekusi query yang telah dibuat dan melakukan commit jika diperlukan."""
        connection = None
        try:
            connection = self.connect_to_database()
            cursor = connection.cursor()
            self.run_query(cursor)
            self.dumpSQL(connection) # dump to .txt file
            return self.handle_query_results(cursor, commit, connection)
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    def connect_to_database(self):
        """Membuat koneksi ke database berdasarkan konfigurasi."""
        if self.postgresql_url:
            return psycopg2.connect(self.postgresql_url)
        else:
            return sqlite3.connect(self.sqlite_path)

    def run_query(self, cursor):
        """Menjalankan query yang telah disiapkan dengan atau tanpa nilai terikat."""
        if self.values is not None:
            # print(self.query, self.values)
            cursor.execute(self.query, self.values)
        else:
            # print(self.query)
            cursor.execute(self.query)

    def handle_query_results(self, cursor, commit, connection):
        """Mengelola hasil dari query yang dijalankan."""
        if not commit:
            return cursor.fetchall()
        else:
            connection.commit()
            return None
        
    def dumpSQL(self, connection):
        with open('sqlite_values.txt', 'w') as f:
            for line in connection.iterdump():
                f.write('%s\n' % line)


