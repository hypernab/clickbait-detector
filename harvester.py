import feedparser
import pandas as pd
import urllib.request
import time

BROWSER_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

# ─────────────────────────────────────────────
#  ADD OR REMOVE SOURCES HERE
#  0 = real/standard news
#  1 = clickbait/tabloid/gossip
# ─────────────────────────────────────────────
SOURCES = {
    # Standard news
    "https://feeds.npr.org/1001/rss.xml":                        0,
    "https://feeds.bbci.co.uk/news/rss.xml":                     0, 
    "https://abcnews.go.com/abcnews/topstories":                  0, 
    "https://feeds.nbcnews.com/nbcnews/public/news":              0, 
    "https://cbsnews.com/latest/rss/main":                        0, 
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml": 0, 
    "https://feeds.washingtonpost.com/rss/national":              0, 
    "https://feeds.skynews.com/feeds/rss/world.xml":             0,
    "https://www.theguardian.com/world/rss":                     0, 

    # Clickbait / tabloid
    "https://www.dailymail.co.uk/articles.rss":                  1,
    "https://www.mirror.co.uk/news/rss.xml":                     1,
    "https://nypost.com/feed/":                                  1,  
    "https://tmz.com/rss.xml":                                   1,  
    "https://perezhilton.com/feed":                              1, 
    "https://hollywoodlife.com/feed":                            1,
    "https://www.usmagazine.com/feed":                           1,  
    "https://justjared.com/feed":                                1,
    "https://www.buzzfeed.com/index.xml":                        1,
}


def get_feed(url):
    try:
        request = urllib.request.Request(url, headers=BROWSER_HEADER)
        response = urllib.request.urlopen(request, timeout=10)
        raw_xml = response.read()
        return feedparser.parse(raw_xml).entries
    except Exception as error:
        print(f"   ⚠️  Skipped ({error})")
        return []


def collect_headlines():
    all_stories = []

    print("🚀 Headline Harvester starting...")
    print(f"   Pulling from {len(SOURCES)} sources\n")

    for url, label in SOURCES.items():
        source_type = "Standard" if label == 0 else "Clickbait"
        print(f"📡 [{source_type}] {url}")

        articles = get_feed(url)

        for article in articles:
            if not article.get("title"):
                continue
            all_stories.append({
                "headline": article["title"].strip(),
                "label":    label,
            })

        print(f"   ✔  {len(articles)} headlines grabbed")
        time.sleep(2)

    if not all_stories:
        print("\n❌ Nothing collected - check your internet connection.")
        return

    df = pd.DataFrame(all_stories)
    df = df.drop_duplicates(subset=["headline"]).reset_index(drop=True)

    output_file = "clickbait.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    counts = df["label"].value_counts().sort_index()

    print("\n" + "─" * 40)
    print(f"✅ Done!  Saved to: {output_file}")
    print(f"📊 Total headlines: {len(df)}")
    print(f"   Standard news:  {counts.get(0, 0)}")
    print(f"   Clickbait:      {counts.get(1, 0)}")
    print("─" * 40)

collect_headlines()