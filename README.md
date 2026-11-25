# Database Lab 5 - Part II

Library website using Flask and MySQL, continued from Lab 4 with reviews and the new queries.

**Team:**
- Mahmoud Hassan Elragal - 2304247
- Marwan Tamer Hassan - 2304015

## How to run

Requires Python 3 and MySQL 8.0.31 or newer. Run the commands from the project folder.

**1. Install the packages**

```powershell
python -m pip install -r website/requirements.txt
```

**2. Create the databases and load the data**

```powershell
mysql -u root -p
```

Inside the MySQL client, run:

```sql
SOURCE website/database/schema.sql;
SOURCE problem2_DDL.sql;
SOURCE problem2_DML.sql;
SOURCE problem2_Queries.sql;
exit;
```

The DDL resets the `library` database. Run the DML once after it.

**3. Set up the connection**

For a new setup, copy `website/.env.example` to `website/.env`. Enter your MySQL username, password and port, and replace `SECRET_KEY` with a random value. Use `DB_NAME=registration` and `LIBRARY_DB_NAME=library` for the databases created above.

**4. Start the website**

```powershell
python website/app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000), register or log in, then click **Library**. The Lab 5 pages are under **Library insights**. The Lab 4 pages are still available.

## Queries and bonus

The queries for F2.1-F2.6 are in `problem2_Queries.sql`. The `book_details` view is created in `problem2_DDL.sql` and used in F2.1 and both parts of F2.3 for the bonus.
