import feedparser
import urllib.parse


def lookup(geo):
    """Look up articles for geo"""

    # Check cache
    try:
        if geo in lookup.cache:
            return lookup.cache[geo]
    except AttributeError:
        lookup.cache = {}

    # Replace special characters
    escaped = urllib.parse.quote(geo, safe="")

    # Get feed from Google
    feed = feedparser.parse(f"https://news.google.com/news/rss/local/section/geo/{escaped}")

    # If no items in feed, get feed from Onion
    if not feed["items"]:
        feed = feedparser.parse("http://www.theonion.com/feeds/rss")

    # Cache results
    lookup.cache[geo] = [{"link": item["link"], "title": item["title"]} for item in feed["items"]]

    # Return results
    return lookup.cache[geo]

def cleaner(q):
    if "," in q:
        ql = q.split(",")
        ql = [i.strip()for i in ql]

    else:
        if q[-1].isupper() == True and q[-2].isupper() == True:
            state_code = q[-2] + q[-1]
            ql =[q[:-2],state_code]
        else:
            ql =[q]
    return ql



