#!/usr/bin/env python3
'''
Stats about Nginx logs
stored in MongoDB
'''


from pymongo import MongoClient


def log_stats():
    """
    Connects to the MongoDB database,
    retrieves Nginx log data, and prints
    various statistics about the logs.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count number of logs for each HTTP method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Define the query for status checks
    status_check_query = {"method": "GET", "path": "/status"}

    status_check = collection.count_documents(status_check_query)
    print(f"{status_check} status check")


if __name__ == "__main__":
    log_stats()
