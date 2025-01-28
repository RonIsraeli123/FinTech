from pymongo import MongoClient

connection_string = "mongodb+srv://stamdvarim1000:zYFKmUxwyYNhpXSX@main.6juz9.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

client = MongoClient(connection_string)

db = client["budget"]

collection = db["test_budget_collection"]
