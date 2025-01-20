import sqlite3
import logging

class DatabaseManager:
    def __init__(self, database_path):
        self.database_path = database_path

    def get_existing_publications(self, author_id):
        """Fetch existing publications for the author from the database."""
        conn = sqlite3.connect(self.database_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT doi FROM publications WHERE author_id = ?;", (author_id,))
            return {row[0] for row in cursor.fetchall()}
        finally:
            cursor.close()
            conn.close()
            
    def add_publication(self, publication):
        """Insert a publication into the database."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO publications (doi, author_id, title) VALUES (?, ?, ?);",
            (publication['doi'], publication['author_id'], publication['title'])
        )
        conn.commit()  # Commit after each insert
        conn.close()

    def get_author_name_by_id(self, author_id):
        """Fetch the author_name corresponding to a given author_id from the Researchers table."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        query = "SELECT NameFull FROM Researchers WHERE uniqname = ?"
        cursor.execute(query, (author_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            logging.warning(f"No author found with author_id: {author_id}")
            return None

    def get_author_id_by_name(self, author_name):
        """
        Fetch the author_id (uniqname) corresponding to a given author_name from the Researchers table.
        
        Args:
            author_name (str): The full name of the author to look up
            
        Returns:
            str or None: The author's uniqname if found, None otherwise
        """
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        query = "SELECT uniqname FROM Researchers WHERE NameFull = ?"
        cursor.execute(query, (author_name,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        else:
            logging.warning(f"No author found with name: {author_name}")
            return None

    def get_all_authors(self):
        """Fetches all author IDs from the Researchers table."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT uniqname FROM Researchers;")
        names = cursor.fetchall()
        conn.close()
        if names:
            return [name[0] for name in names]
        else:
            logging.info("No researchers found.")
            return []
    
    def add_expert_field(self, expfield):
        """
        Insert an experimental field entry into the database.
        
        Args:
            expfield (dict): Dictionary containing expfields, tagname, and author_id
        """
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO ExpFields (expfields, tagname, author_id) VALUES (?, ?, ?);",
            (expfield['expfields'], expfield['tagname'], expfield['author_id'])
        )
        
        conn.commit()  # Commit the transaction
        conn.close()

    def add_researcher(self, info):
        """Insert a researcher into Researcher database"""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO researchers (Uniqname,Centers,statusResearcher,NameFull,LastName,NameFullReverse,Phone,slug,kp,profilePage,email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10], info[11])
        )
        conn.commit()  # Commit after each insert
        conn.close()