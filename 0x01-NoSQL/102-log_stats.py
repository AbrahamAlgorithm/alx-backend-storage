#!/usr/bin/env python3
"""
Script to provide statistics about Nginx logs stored in MongoDB.
Includes:
- Total number of logs
- Counts for different HTTP methods (GET, POST, etc.)
- Counts for requests to /status endpoint
- Top 10 IPs by frequency
"""

from pymongo import MongoClient

def print_logs_stats(collection):
    # Total number of logs
    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    # Count methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count /status endpoint requests
    status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    # Top 10 IPs by frequency
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(collection.aggregate(pipeline))
    for idx, ip in enumerate(top_ips, start=1):
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_db = client.logs
    nginx_collection = logs_db.nginx

    print_logs_stats(nginx_collection)

