from itemadapter import ItemAdapter
import sqlite3


class DatabasePipeline:
    # Database setup
    conn = sqlite3.connect('eximbank.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute(""" CREATE TABLE IF NOT EXISTS articles 
        (title text, year text, link text) """)

    def process_item(self, item, spider):
        self.c.execute("""SELECT * FROM articles WHERE title = ? AND year = ?""",
                       (item.get('title'), item.get('year')))
        duplicate = self.c.fetchall()
        if len(duplicate):
            return item
        print(f"New entry added at {item['link']}")

        # Insert values
        self.c.execute("INSERT INTO articles (title, year, link)"
                       " VALUES (?,?,?)", (item.get('title'), item.get('year'), item.get('link')))
        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
