#!/usr/bin/python3
import requests

def count_words(subreddit, word_list, after=None, count={}):
    if not word_list:
        sorted_counts = sorted(count.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")
        return

    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"

    headers = {"User-Agent": "Mozilla/5.0"}  # Add a User-Agent header to avoid 429 error

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code != 200:
        print("Invalid subreddit or no posts match.")
        return

    articles = data["data"]["children"]
    for article in articles:
        title = article["data"]["title"].lower()
        for word in word_list:
            if (
                word.lower() in title
                and not title.endswith((".", "!", "_"))
                and word not in {"java", "javascript"}
            ):
                count[word.lower()] = count.get(word.lower(), 0) + 1

    after = data["data"]["after"]
    count_words(subreddit, word_list, after, count)

