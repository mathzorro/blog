"""Reconstruct self-authored threads from a Twitter/X archive.

Usage:
    python extract_threads.py path/to/archive [--out threads.json]

`path/to/archive` is the unzipped archive folder (containing data/tweets.js
and data/tweets_media/). Writes a JSON file with one entry per thread:
tweets in order, text with HTML entities decoded, t.co links expanded,
and media mapped to their files in data/tweets_media/.
"""
import argparse, html, json, re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def load_tweets(archive):
    data_dir = Path(archive) / "data"
    tweets = {}
    for f in sorted(data_dir.glob("tweets*.js")):
        raw = f.read_text(encoding="utf-8")
        for item in json.loads(raw[raw.index("["):]):
            t = item["tweet"]
            tweets[t["id_str"]] = t
    return tweets


def created(t):
    return datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S %z %Y")


def clean_text(t):
    """Decode entities, expand links, drop media placeholder links."""
    text = html.unescape(t["full_text"])
    for u in t["entities"].get("urls", []):
        text = text.replace(u["url"], u["expanded_url"])
    for m in t.get("extended_entities", {}).get("media", []):
        text = text.replace(m["url"], "")
    return text.strip()


def media_files(t, media_dir):
    out = []
    for m in t.get("extended_entities", {}).get("media", []):
        name = m["media_url_https"].rsplit("/", 1)[-1]
        pattern = f"{t['id_str']}-{Path(name).stem}*"
        matches = sorted(p.name for p in media_dir.glob(pattern))
        out.append({"type": m["type"],
                    "archive_file": matches[0] if matches else None,
                    "expected_name": f"{t['id_str']}-{name}"})
    return out


def build_threads(tweets):
    children = defaultdict(list)
    for tid, t in tweets.items():
        parent = t.get("in_reply_to_status_id_str")
        if parent in tweets:  # reply to one of my own tweets
            children[parent].append(tid)
    replies = {c for kids in children.values() for c in kids}
    threads = []
    for root in children:
        if root in replies:
            continue
        seq, stack = [], [root]
        while stack:
            cur = stack.pop(0)
            seq.append(cur)
            kids = sorted(children.get(cur, []), key=lambda k: created(tweets[k]))
            stack = kids + stack
        threads.append(seq)
    threads.sort(key=lambda s: created(tweets[s[0]]))
    return threads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("--out", default="threads.json")
    args = ap.parse_args()

    tweets = load_tweets(args.archive)
    media_dir = Path(args.archive) / "data" / "tweets_media"
    result = []
    for seq in build_threads(tweets):
        root = tweets[seq[0]]
        result.append({
            "root_id": seq[0],
            "date": created(root).date().isoformat(),
            "num_tweets": len(seq),
            "likes": sum(int(tweets[i]["favorite_count"]) for i in seq),
            "reply_to_other": bool(root.get("in_reply_to_screen_name")),
            "tweets": [{"id": i, "text": clean_text(tweets[i]),
                        "media": media_files(tweets[i], media_dir)} for i in seq],
        })
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False),
                              encoding="utf-8")
    print(f"{len(tweets)} tweets, {len(result)} threads -> {args.out}")


if __name__ == "__main__":
    main()
