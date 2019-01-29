from django.db import connection


def print_queries():
    for q in connection.queries:
        print q
        print '-' * 80



