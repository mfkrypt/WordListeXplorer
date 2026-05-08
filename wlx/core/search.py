from wlx.core import db


def search_wordlists(query: str, tags: list[str] = None):
    return db.search_wordlists(query, tags)