import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase URL or API Key in environment variables.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_user_account(email: str, pswd: str, name: str, business_name: str, role: str):
    """
    Inserts a user account into the Supabase database.

    :param email: Email of the user (non-nullable). 
    :param pswd: Password of the user (non-nullable).
    :param name: Name of the user (non-nullable).
    :param business_name: Business name (nullable).
    :param role: Role of the user ('USER' or 'BUSINESS').
    """
    data = {
        "email": email,
        "password": pswd,
        "name": name,
        "businessname": business_name,
        "role": role
    }

    response = supabase.table("account").insert(data).execute()

    if response.status_code == 201:
        print("User account inserted successfully.")
    else:
        print("Failed to insert user account:", response.data)

# Example usage
if __name__ == "__main__":
    # Replace with actual values
    insert_user_account(email="bob@gmail.com", pswd="123456", name="Bob", business_name=None, role="USER")