import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host="localhost", user="root", password="Newton 123", database="cloth_design_database"):
        """Initialize the database connection."""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()

            # Ensure the tables are created
            # self.create_tables()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None
            self.cursor = None

    def create_tables(self):
        """Create the tables if they don't exist."""
        if self.conn and self.cursor:
            # Create product_details table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_detail (
                    Product_id INT AUTO_INCREMENT PRIMARY KEY,
                    Product_image Text,
                    Product_link VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
                    Product_price VARCHAR(255),
                    Product_size TEXT,
                    Product_name VARCHAR(255)
                )
            """)

    def is_link_existing(self, link):
        """Check if the product link already exists in both tables."""
        if not self.conn or not self.cursor:
            return False

        # Check in product_description table
        self.cursor.execute("SELECT 1 FROM product_description WHERE Product_link = %s", (link,))
        if self.cursor.fetchone():
            print("true")
            return True
            

        # Check in product_detail table
        self.cursor.execute("SELECT 1 FROM product_detail WHERE Product_link = %s", (link,))
        if self.cursor.fetchone():
            return True

        return False
    # def is_link_existing(self, link):
    #     """Check if the product link already exists in both tables."""
    #     if not self.conn or not self.cursor:
    #         print("Database connection or cursor is not initialized.")
    #         return False

    #     try:
    #         # Debugging: Print the link being checked
    #         print(f"Checking existence for link: {link}")

    #         # Check in product_description table
    #         query_description = "SELECT 1 FROM product_description WHERE Product_link = %s"
    #         self.cursor.execute(query_description, (link,))
    #         result_description = self.cursor.fetchone()

    #         # Debugging: Log the query and result
    #         print(f"Executed query: {query_description} with parameter: {link}")
    #         print(f"Result from product_description: {result_description}")

    #         if result_description:
    #             return True

    #         # Check in product_detail table
    #         query_detail = "SELECT 1 FROM product_detail WHERE Product_link = %s"
    #         self.cursor.execute(query_detail, (link,))
    #         result_detail = self.cursor.fetchone()

    #         # Debugging: Log the query and result
    #         print(f"Executed query: {query_detail} with parameter: {link}")
    #         print(f"Result from product_detail: {result_detail}")

    #         if result_detail:
    #             return True

    #         return False

        # except Error as e:
        #     # Debugging: Log any SQL errors
        #     print(f"Error while checking link existence: {e}")
        #     return False


    def save_product_links(self, product_links):
        """Save product links to both tables."""
        if not self.conn or not self.cursor:
            return

        for link in product_links:
            # Check if the link already exists
            if not self.is_link_existing(link):
                # Insert the product link into the product_description table
                self.cursor.execute("INSERT INTO product_description (Product_link) VALUES (%s)", (link,))
                # Insert the product link into the product_detail table
                self.cursor.execute("INSERT INTO product_detail (Product_link) VALUES (%s)", (link,))
                print(f"Saved new link: {link}")
            else:
                print(f"Link already exists: {link}")

        self.conn.commit()

    
    def save_product_details(self, product_details):
        if not self.conn or not self.cursor:
            print("Database connection not initialized.")
            return

        for detail in product_details:
            # print(f"Processing details for: {detail['url']}")
            # if not self.is_link_existing(detail["url"]):
            #     print(f"Skipping link (not in description): {detail['url']}")

            try:
                # Update product_detail
                # self.cursor.execute("""
                # INSERT INTO product_detail(product_name, product_price, product_size, product_image)
                # values("owais", 69420, 9000, 'abc');
                # """)
                #inserting in the database tablename(product-detail)
                self.cursor.execute("""
                INSERT INTO product_detail(product_name, product_price, product_size, product_image, product_link)
                values("%s", %s, %s, %s,%s); """, (detail["name"], (detail["price"]), ','.join(detail["size"]), detail["image"], detail["url"]))
                #inserting in the database tablename(product-description)
                self.cursor.execute("""
                INSERT INTO product_description(product_description, product_link)
                values("%s", %s); """, (detail["description"], (detail["url"])))
                self.conn.commit()

            except Error as e:
                print(f"SQL Error: {e}")

        # self.conn.commit()
        print("All product details saved.")

    def get_all_product_links(self):
        """Retrieve all product links from both tables."""
        if not self.conn or not self.cursor:
            return []

        self.cursor.execute("SELECT Product_link FROM product_description")
        description_links = self.cursor.fetchall()

        self.cursor.execute("SELECT Product_link FROM product_detail")
        details_links = self.cursor.fetchall()

        # Combine the links from both tables
        all_links = set(link[0] for link in description_links + details_links)
        return all_links

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            