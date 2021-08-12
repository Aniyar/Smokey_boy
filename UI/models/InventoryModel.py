class InventoryModel:
    def __init__(self, connection):
        self.connection = connection

    def get_connection(self):
        return self.connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(50),
                             class VARCHAR(1),
                             availability INTEGER(1),
                             location VARCHAR(128),
                             description VARCHAR(258)
                             )''')
        # cursor.close()
        self.connection.commit()

    def insert(self, name, Class, availability, location, description=""):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO inventory 
                          (name, class, availability, location, description) 
                          VALUES (?,?,?,?,?)''''''''''', (name, Class, availability, location, description))
        # cursor.close()
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        return rows

    def get_available(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM inventory WHERE availability = 1")
        rows = cursor.fetchall()
        return rows

    def get_unavailable(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM inventory WHERE availability = 0")
        rows = cursor.fetchall()
        return rows


    def change_location(self, id, new_loc):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE inventory 
                            SET location = ?
                            WHERE id = ?;''', (new_loc, id))
        # cursor.close()
        self.connection.commit()

    def change_availability(self, id, new_ava):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE inventory 
                            SET availability = ?
                            WHERE id = ?;''', (new_ava, id))
        # cursor.close()
        self.connection.commit()


    def delete(self, item_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM inventory WHERE id = ?''', (str(item_id),))
        cursor.close()
        self.connection.commit()