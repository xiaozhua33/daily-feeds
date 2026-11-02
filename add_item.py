#!/usr/bin/env python3
"""用法: python3 add_item.py <feed: ai|trade> <标题> <正文文件路径>
把一篇早报加到 feed，最多保留 10 篇，然后提交并推送。"""
import sys, html, datetime, subprocess, json, os
feed, title, body_path = sys.argv[1], sys.argv[2], sys.argv[3]
names = {"ai": "AI 新动向入门早报", "trade": "交易入门早报"}
base = "https://xiaozhua33.github.io/daily-feeds"
os.chdir(os.path.dirname(os.path.abspath(__file__)))
store = f"{feed}.json"
items = json.load(open(store)) if os.path.exists(store) else []
body = open(body_path, encoding="utf-8").read().strip()
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
iid = now.strftime("%Y%m%d%H%M%S")
items.insert(0, {"id": iid, "title": title, "body": body, "date": now.strftime("%a, %d %b %Y %H:%M:%S +0900")})
items = items[:10]
json.dump(items, open(store, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
os.makedirs(feed, exist_ok=True)
out = []
for it in items:
    paras = "".join(f"<p>{html.escape(p)}</p>" for p in it["body"].split("\n") if p.strip())
    link = f"{base}/{feed}/{it['id']}.html"
    open(f"{feed}/{it['id']}.html", "w", encoding="utf-8").write(
        f"<!doctype html><meta charset=utf-8><title>{html.escape(it['title'])}</title><article><h1>{html.escape(it['title'])}</h1>{paras}</article>")
    out.append(f"<item><title>{html.escape(it['title'])}</title><link>{link}</link><guid>{link}</guid><pubDate>{it['date']}</pubDate><description><![CDATA[{paras}]]></description></item>")
rss = f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{names[feed]}</title><link>{base}/</link><description>{names[feed]}</description><language>zh-cn</language>{"".join(out)}</channel></rss>'
open(f"{feed}.xml", "w", encoding="utf-8").write(rss)
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-qm", f"{feed}: {title}"], check=True)
subprocess.run(["git", "push", "-q"], check=True)
print(f"{base}/{feed}.xml")
