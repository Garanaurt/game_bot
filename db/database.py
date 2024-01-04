import sqlite3

db_path = 'DATABASE.db'

class DbShop:
    def __init__(self) -> None:
        self.db_path = None

    def db_initialize(self):
        print('Database was started')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def db_close_conn(self):
        print('Database was closed')
        self.conn.close()



    def db_add_message_in_messages(self, chat_id, message_id):
        self.cursor.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", (chat_id, message_id))
        self.conn.commit()
        return True
    

    def db_get_messages_in_chat(self, chat):
        self.cursor.execute("SELECT * FROM messages WHERE user_id = ?", (chat,))
        result = self.cursor.fetchall()
        return result


    def db_delete_message_in_chat(self, chat):
        self.cursor.execute("DELETE FROM messages WHERE user_id = ?", (chat,))
        self.conn.commit()
        return True
    



    def db_add_message_in_messages_admin(self, chat_id, message_id):
        self.cursor.execute("INSERT INTO admin_messages (user_id, message) VALUES (?, ?)", (chat_id, message_id))
        self.conn.commit()
        return True
    

    def db_get_messages_in_chat_admin(self, chat):
        self.cursor.execute("SELECT * FROM admin_messages WHERE user_id = ?", (chat,))
        result = self.cursor.fetchall()
        return result


    def db_delete_message_in_chat_admin(self, chat):
        self.cursor.execute("DELETE FROM admin_messages WHERE user_id = ?", (chat,))
        self.conn.commit()
        return True




















    def db_get_all_games(self):
        self.cursor.execute("SELECT * FROM games")
        result = self.cursor.fetchall()
        return result
    


    def db_add_game_to_db(self, game):
        name = game['name']
        image_path = game['image_path']
        description = game['description']
        instruction = game['instruction']
        descriptionrf = game['descriptionrf']
        instructionrf = game['instructionrf']
        self.cursor.execute("INSERT INTO games (name, image_path, description, instruction, description_rf, instruction_rf) VALUES (?, ?, ?, ?, ?, ?)", 
                            (name, image_path, description, instruction, descriptionrf, instructionrf))
        self.conn.commit()



    def db_delete_game(self, game_id):
        self.cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self.conn.commit()



    def db_get_game_where_id(self, game_id):
        self.cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        result = self.cursor.fetchone()
        return result
    

    def db_set_game_name_where_id(self, game_id, name):
        self.cursor.execute("UPDATE games SET name = ? WHERE id = ?", (name, game_id))
        self.conn.commit()


    def db_set_game_description_where_id(self, game_id, description):
        self.cursor.execute("UPDATE games SET description = ? WHERE id = ?", (description, game_id))
        self.conn.commit()


    def db_set_game_description_rf_where_id(self, game_id, description_rf):
        self.cursor.execute("UPDATE games SET description_rf = ? WHERE id = ?", (description_rf, game_id))
        self.conn.commit()


    def db_set_game_instruction_where_id(self, game_id, instruction):
        self.cursor.execute("UPDATE games SET instruction = ? WHERE id = ?", (instruction, game_id))
        self.conn.commit()

    
    def db_set_game_instructionrf_where_id(self, game_id, instructionrf):
        self.cursor.execute("UPDATE games SET instruction_rf = ? WHERE id = ?", (instructionrf, game_id))
        self.conn.commit()


    def db_set_game_image_where_id(self, game_id, file_path):
        self.cursor.execute("UPDATE games SET image_path = ? WHERE id = ?", (file_path, game_id))
        self.conn.commit()


    def db_check_and_create_tables(self):
        print('create db')
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            name TEXT,                
            image_path TEXT,
            description TEXT,
            instruction TEXT,
            description_rf TEXT,
            instruction_rf TEXT               
            );""")
        self.conn.commit()
        print('Table games was created')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_messages (
            user_id INTEGER,
            message TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
            )''')
        self.conn.commit()
        print('Table admin_messages was created')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
            user_id INTEGER,
            message TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
            )''')
        self.conn.commit()
        print('Table messages was created')



