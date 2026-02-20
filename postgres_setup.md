# PostgreSQL 18 Setup and Running schema.sql

1. **Install PostgreSQL**
   - Download PostgreSQL from the official website: https://www.postgresql.org/download/
   - During installation:
     - Set a password for the `postgres` user (remember this password).
     - Ensure the **Command Line Tools** option is selected.
     - Note the installation directory (e.g., `C:\Program Files\PostgreSQL\18`).

2. **Add PostgreSQL to PATH (Optional)**
   - Open "Environment Variables" settings on your system.
   - Under "System Variables," find the `Path` variable and click **Edit**.
   - Add the path to the PostgreSQL `bin` directory (e.g., `C:\Program Files\PostgreSQL\18\bin`).
   - Save the changes and restart your terminal.

3. **Open psql**
   - Open your terminal (e.g., PowerShell or Command Prompt).
   - Run the following command to connect to PostgreSQL:
     ```
     &"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres
     ```
   - Enter the password for the `postgres` user when prompted.

4. **Create a New Database**
   - Once connected to `psql`, create a new database:
     ```
     CREATE DATABASE event_waitlist;
     ```
   - Connect to the new database:
     ```
     \c event_waitlist
     ```

5. **Run the `schema.sql` File**
   - Navigate to the directory containing the `schema.sql` file:
     ```
     cd C:\Users\...\T12_SeniorProject\backend
     ```
   - Run the `schema.sql` file using the `\i` command:
     ```
     \i 'C:/Users/.../T12_SeniorProject/backend/schema.sql'
     ```

6. **Verify the Schema**
   - After running the script, check if the tables were created successfully:
     ```
     \dt
     ```
   - This will display a list of all tables in the current database.

7. **Exit psql**
   - When you're done, exit the `psql` shell by typing:
     ```
     \q
     ```

8. **Optional: Run the `schema.sql` File Directly**
   - If you don’t want to open the `psql` shell, you can run the `.sql` file directly from the terminal:
     ```
     "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d event_waitlist -f [schema.sql](http://_vscodecontentref_/1)
     ```
   - Replace `postgres` with your username and `event_waitlist` with your database name.
   - Ensure the `schema.sql` file is in the current directory, or provide the full path to the file.

---

# Notes:
- Use forward slashes (`/`) in file paths when using the `\i` command in `psql`.
- If you encounter issues with the `psql` command not being recognized, ensure PostgreSQL is installed correctly and the `bin` directory is added to your PATH environment variable.
- If you forget the `postgres` password, you can reset it using the **pgAdmin** tool or by modifying the PostgreSQL configuration files.
