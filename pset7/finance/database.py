from cs50 import SQL
from helpers import lookup
db = SQL("sqlite:///finance.db")

rows = db.execute("SELECT DISTINCT stock_name, SUM(shares) AS total FROM portifolio WHERE user_id  = 20000000")

print(rows)
