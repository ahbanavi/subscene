import logging
import os
import re
import sys

import mariadb
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SUBS_PATH = os.getenv("SUBS_PATH", "./Subscene Files DB")

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="tg.log",
    filemode="a",
)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME", "subscene"),
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


conn.autocommit = True

# Get Cursor
cur = conn.cursor(dictionary=True)


# get all subs that lang = farsi_persian
cur.execute(
    "SELECT * FROM all_subs WHERE lang = 'farsi_persian' AND tg_post_id IS NULL ORDER BY fileLink,title"
)


def strip_html(text):
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")


def upload():
    for sub in cur.fetchall():
        with open(f"{SUBS_PATH}/{sub['fileLink']}", "rb") as f:
            caption_list = []
            if sub["title"]:
                caption_list.append(f"📽 <b>{strip_html(sub['title'])}</b>")

            if sub["author_name"]:
                caption_list.append(f"✍️ <i>{strip_html(sub['author_name'])}</i>")

            if sub["imdb"]:
                caption_list.append(
                    f"🎥 <a href='https://www.imdb.com/title/tt{sub['imdb']}'>IMDb</a> | <code>tt{sub['imdb']}</code>"
                )

            caption_list.append(f"🆔 <code>{sub['id']}</code>")

            if sub["date"]:
                caption_list.append(f"📅 {sub['date']}")

            if sub["comment"]:
                caption_list.append(f"💬 {strip_html(sub['comment'])}")

            release = strip_html(sub["releases"])

            release = release.translate({ord(i): None for i in '[",]'}).strip("-_ ")
            if release:
                caption_list.append(f"<pre>{release}</pre>")

            caption = "\n".join(caption_list)

            if len(caption) > 1000:
                caption = caption[:1000]
                if release:
                    if caption.count("<pre>") == 1 and caption.count("</pre>") == 0:
                        caption += "</pre>"

            files = {"document": f}
            params = {
                "chat_id": CHANNEL_ID,
                "caption": caption,
                "parse_mode": "HTML",
            }
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                files=files,
                params=params,
            )
            if response.status_code == 200:
                cur.execute(
                    "UPDATE all_subs SET tg_post_id = ? WHERE id = ? LIMIT 1",
                    (response.json()["result"]["message_id"], sub["id"]),
                )
            else:
                logging.error(
                    f"Error uploading {sub['title']}, id: {sub['id']}: {response.text}"
                )


upload()
