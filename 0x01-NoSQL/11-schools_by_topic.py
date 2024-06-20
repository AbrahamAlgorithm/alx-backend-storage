#!/usr/bin/env python3
'''
Where can I learn Python?
'''


def schools_by_topic(mongo_collection, topic):
    '''
    Python function that returns
    the list of school having
    a specific topic
    '''
    return list(mongo_collection.find({"topics": topic}))
