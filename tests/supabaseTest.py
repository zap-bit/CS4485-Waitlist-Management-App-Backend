import os
from supabase import create_client, Client
from dotenv import load_dotenv
import hashlib
import time

# Load environment variables from .env file
load_dotenv()

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase URL or API Key in environment variables.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_user_account(name, email, pswd, phone):
    hashed_password = hash_password(pswd)
    data = {
        "name": name,
        "account_type": "USER",
        "email": email,
        "password": hashed_password,
        "phone": phone,
        "business_name": None  # USER accounts do not have a business name
    }
    response = supabase.table("account").insert(data).execute()
    return response

def create_bus_account(name, email, pswd, b_name, phone):
    hashed_password = hash_password(pswd)
    data = {
        "name": name,
        "account_type": "BUSINESS",
        "email": email,
        "password": hashed_password,
        "phone": phone,
        "business_name": b_name  # BUSINESS accounts require a business name
    }
    response = supabase.table("account").insert(data).execute()
    return response

# Example usage
if __name__ == "__main__":
    # Example testers for creating tables in Supabase
    print("testing backend/databse connection -Kyle")
    create_user_account("Bob", "bob@gmail.com", "password123", 1112223333)
    create_bus_account("Joe", "joesfood@company.com", "joeshack", "joes food", 1234567890)
