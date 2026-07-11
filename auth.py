import sqlite3

def get_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    return user



def login(user, pwd):
    if user == None:
        return False
    result = get_user(user, pwd)
    if result != None:
        return True


def reset_password(user_id, new_password):
    print("New password is: " + new_password)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET password = '{new_password}' WHERE id = {user_id}")
    conn.commit()