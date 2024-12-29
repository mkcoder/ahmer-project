import sqlite3

class Database:
    def __init__(self, db_name="products.db"):
        """Initialize the database connection."""
        self.db_name = "cloth_design_database"
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Ensure the tables are created
        self.create_tables()
    
    #this function is use for Checking if the product link already exists in both tables: product_description and product_details.
    def is_link_existing(self, link):
        self.cursor.execute("SELECT 1 FROM product_description WHERE product_link = ?", (link,))
        if self.cursor.fetchone():
            return True

        self.cursor.execute("SELECT 1 FROM product_details WHERE product_link = ?", (link,))
        if self.cursor.fetchone():
            return True

        return False
    #this function will Save product links to both tables: product_description and product_details.
    def save_product_links(self, product_links):
        for link in product_links:
            # Check if the link already exists
            if not self.is_link_existing(link):
                # Insert the product link into the product_description table
                self.cursor.execute("INSERT INTO product_description (product_link) VALUES (?)", (link,))
                # Insert the product link into the product_details table
                self.cursor.execute("INSERT INTO product_details (product_link) VALUES (?)", (link,))
            else:
                print(f"Link already exists: {link}")

        self.conn.commit()

    def get_all_product_links(self):
        """Retrieve all product links from both tables."""
        self.cursor.execute("SELECT product_link FROM product_description")
        description_links = self.cursor.fetchall()

        self.cursor.execute("SELECT product_link FROM product_details")
        details_links = self.cursor.fetchall()

        # Combine the links from both tables
        all_links = set(description_links + details_links)
        return all_links

    def close(self):
        """Close the database connection."""
        self.conn.close()

