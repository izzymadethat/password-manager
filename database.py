from pymongo import MongoClient

URI = "mongodb://localhost:27017"
client = MongoClient(URI)

dbs = client.list_database_names()
db = client.password_mgr
users = db.users
passwords = db.password_entries

def get_user_id(email, password):
    user = users.find_one({"email": email, "password": password})
    if user:
        return user["_id"]
    else:
        return None

def authenticate_user(email, password) -> bool:
    user = users.find_one({"email": email, "password": password})
    if user:
        return True
    else:
        return False

def check_if_email_exists(email: str) -> bool:
    user = users.find_one({"email": email})
    if user:
        return True
    else:
        return False

def create_user_upon_signup(email, password):
    users.insert_one({"email": email, "password": password})

def add_password_entry(
    user_id, website, title, username, email, encrypted_password, favorite, notes, date
):
    new_entry = {
        "user_id": user_id,
        "site_details": {
            "website": website,
            "title": title,
            "username": username,
            "email": email,
            "password": encrypted_password,
            "favorite": favorite,
            "notes": notes,
            "last_modified": date + "UTC",
        },
    }

    try:
        entry = passwords.insert_one(new_entry)
        return "Entry Added"
    except Exception as e:
        return f"Error: {str(e)}"
