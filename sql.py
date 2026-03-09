import sqlite3
from collections import Counter

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect('store.db')
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

# Create products table with UNIQUE constraint
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store TEXT NOT NULL,
    total_results INTEGER,
    description TEXT,
    price TEXT,
    link TEXT,
    image_url TEXT,
    UNIQUE(store, description, price, link)
)
''')

# Optional: Clear table to remove old duplicates
c.execute("DELETE FROM products")

# Example: Insert a user
c.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))

# List of products (from your demoProducts array)
products_to_add = [
    {"name": "Lenovo loq", "price": "₹63,490", "store": "Amazon", "url": "https://www.amazon.in/Lenovo-i5-12450HX-39-6cm-300Nits-83GS00CKIN/dp/B0D8L6R3T3/ref=sr_1_2_sspa?crid=1ICTVS37X65GD&dib=eyJ2IjoiMSJ9.mleJApE5zjkFvAp74x59DFDY1FHacDrcT61m-40PTHNlrOdZLGRTNdCXn6yC9tiZR0d0_KYoaf0hgXupUEx0psSnQhjDBs_3Di_jsjcpYGnY2q4NEjr-C_tTFBKvfpRUHxa8b2-Pt2vKdEFHRivakOWNYdNfbqrJYsp27BVRudCLgQun7Xw6zd0Dz68UOLZbwFidZjGoQvbqC8UBciVwRDEkq5imMe16sdjUaOObmh8.9LKwVninSlV8YCCvVbfzF2UMwKOXhACWfJOqiw3W1gQ&dib_tag=se&keywords=lenovo+Loq&nsdOptOutParam=true&qid=1744962224&sprefix=lenovo+loq%2Caps%2C193&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"},
    {"name": "Lenovo loq", "price": "₹57,990", "store": "flipkart", "url": "https://www.flipkart.com/lenovo-loq-intel-core-i5-12th-gen-12450hx-12-gb-512-gb-ssd-windows-11-home-4-graphics-nvidia-geforce-rtx-2050-15iax9d1-gaming-laptop/p/itme3e94a3f73f71?pid=COMHY9Z8AFVPHVJF&lid=LSTCOMHY9Z8AFVPHVJFAMRSWH&marketplace=FLIPKART&q=lenovo+loq&store=4rr%2Ftz1&spotlightTagId=default_BestsellerId_4rr%2Ftz1&srno=s_1_3&otracker=search&otracker1=search&fm=Search&iid=832ce308-c238-4ae8-8627-9d812c6b6f3b.COMHY9Z8AFVPHVJF.SEARCH&ppt=sp&ppn=sp&ssid=2nc2vi6t000000001744962347281&qH=8f35ca78dc0959c0"},
    {"name": "samsung s23", "price": "₹44,999", "store": "flipkart", "url": "https://www.flipkart.com/samsung-galaxy-s23-5g-cream-128-gb/p/itmc77ff94cdf044?pid=MOBGMFFX5XYE8MZN&lid=LSTMOBGMFFX5XYE8MZNRGKCA5&marketplace=FLIPKART&q=samsung+s23&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=4cbeb455-5e4f-403c-bfdf-625bcc9fbec5.MOBGMFFX5XYE8MZN.SEARCH&ppt=hp&ppn=homepage&ssid=nbo0e8d6ls0000001744962690759&qH=1e144c4dcdb9bb43"},
    {"name": "samsung s23", "price": "₹51,199", "store": "Amazon", "url": "https://www.amazon.in/Samsung-Galaxy-Snapdragon-Phantom-Storage/dp/B0BTYX74HZ/ref=sr_1_6?crid=1DGVS0YWMCDSL&dib=eyJ2IjoiMSJ9.tO-uJL8kHxQkPmXD2eApKGPBJW1EhZg2DyLRGEdrsGb6VZUJVJ6X_y88QAMQqBiuEpGBXlUQuifxnMl8KmJ6d2J_WF8mA05fhNo0cGxFJTs7kEnJbpIXBsuu5pwRUfPQFByTYKFUV2ygSoFyT4ABd0Sj2xELdD0cC_6vH1GgqMVnh-zKodEgawy1TU_hYnsqxrvKsrXSlQndcKDBfleCAQ_LA1x9QOrzgESUrbC7T8o.gXiZHiQl9X0qFqHsIIWElblk5nf5gg6RNFmP6R6bdvk&dib_tag=se&keywords=samsung+s23&nsdOptOutParam=true&qid=1744962606&sprefix=samsung+s23%2Caps%2C217&sr=8-6"},
    {"name": "ipad", "price": "₹34,900", "store": "LuLu Hypermart", "url": "https://www.luluhypermarket.in/product/electronic/apple-ipad-10th-gen-64-gb-rom-109-inch-with-wi-fi-only-blue"},
    {"name": "ipad", "price": "₹25,900", "store": "Flipkart", "url": "https://www.flipkart.com/apple-ipad-10th-gen-64-gb-rom-10-9-inch-wi-fi-only-silver/p/itmd486c16ac081f?pid=TABGJ6XUN2YTSBVU&lid=LSTTABGJ6XUN2YTSBVUHSF9US&marketplace=FLIPKART&q=ipad&store=tyy%2Fhry&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=4bc50a0f-5a46-47b5-9194-8ce3356bac2a.TABGJ6XUN2YTSBVU.SEARCH&ppt=pp&ppn=pp&ssid=2ycbgjc3tc0000001744962961392&qH=09401fded433c347"},
    {"name": "iPhone 16", "price": "$150.00", "store": "ebay", "url": "https://www.ebay.com/itm/388274057291?_skw=iphone+16&epid=8071466776&itmmeta=01JS3YQDD5PVEJRCVC6CTX5A1K&hash=item5a66eff04b:g:wZUAAeSwBKdn~8vi&itmprp=enc%3AAQAKAAAA4FkggFvd1GGDu0w3yXCmi1fMf2PTw0%2FU0vqtsmls8dxZumII8HwD8LnnmMDxjrxKb%2BKTPleatMjrI5PySBExJKJQ06Yb8pEHt1%2FCVCcf3Avn9XBC5N%2F8%2BUSJ5pFCpUGGCe1gFMGSTYfo5ISzuYatnzcKD2dZIRfsoLAxxlDBgZ4TlpfxPwaGHjMr0%2FKF6METdGTHneGqKQr91%2BlRynrnPO1ZjeRo1QXOu5%2Blw1FgcbUaMUSp5L1I7pli6fefmNwRInf%2B5AwdQA%2BRsSQjOpR0g68dVlvoAAB5bpKYKwhAgSvV%7Ctkp%3ABk9SR-TW3f7IZQ"},
    {"name": "iPhone 16", "price": "₹74,990", "store": "flipcart", "url": "https://www.flipkart.com/apple-iphone-16-pink-128-gb/p/itmc2e910b4d0b1c?pid=MOBH4DQFWJVDRSHM&lid=LSTMOBH4DQFWJVDRSHMQYAA7N&marketplace=FLIPKART&q=iphone+16&store=tyy%2F4io&spotlightTagId=default_BestsellerId_tyy%2F4io&srno=s_1_3&otracker=search&otracker1=search&fm=Search&iid=ea639b5f-6640-4638-a998-4a3d5c2cca78.MOBH4DQFWJVDRSHM.SEARCH&ppt=sp&ppn=sp&ssid=u1xtvxqvtc0000001744963514770&qH=9ea15d2374058112"},
    {"name": "airpods pro", "price": "$189.99", "store": "bestbuy", "url": "https://www.bestbuy.com/site/apple-airpods-pro-2-wireless-active-noise-cancelling-earbuds-with-hearing-aid-feature-white/6447382.p?skuId=6447382"},
    {"name": "airpods pro", "price": "₹1,199", "store": "flipkart", "url": "https://www.flipkart.com/scubel-airpro-pods-2nd-generation-name-change-gps-popup-ios-bluetooth/p/itmee398ea92478d?pid=ACCHB3HVJ4DNAWKT&lid=LSTACCHB3HVJ4DNAWKTY4X45I&marketplace=FLIPKART&q=air+pods+pro&store=0pm%2Ffcn%2F821%2Fa7x%2F2si&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_9_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_9_na_na_na&fm=search-autosuggest&iid=en_sRpD9ug7QGI2ZHJKf0Qe28PXVVlGsD8PB44LaJwQcweQJgVTwwMsGhLhT_7BeOI3hlhzX0-be-2eQZlE5ffqHw%3D%3D&ppt=sp&ppn=sp&ssid=09l1tm1bu80000001744963931691&qH=5fec2928abe4f6fc"},
    {"name": "lg tv", "price": "₹37,990", "store": "Amazon", "url": "https://www.amazon.in/LG-inches-Ready-Smart-32LM563BPTC/dp/B08DPLCM6T/ref=sr_1_2_sspa?dib=eyJ2IjoiMSJ9.7c7oAGMDMbkdJ_yZ4KVZQxMhiU-iToOxhK-JNUbxJbhGrwDyU1SZ8UEIg6KouX6qEkhOTtM2jagJpYkBe7YNhQMEf_t8GGGYIJNXg_88s-9icloHYyYPG3raGHcvgyS9x5uQn6RNRkdezWeio67wDFZ1GhnJEponR4UDV9806eD4Po0Y_iDWcr_VQMA9sZibQIpHneltctMCPwjDL3ngY9zn-5I41ivBX3dcRexhxN0.I1aCIjKWfzumY1Oi8lHtpzJBfM5fn9exDOiuZ8e97f4&dib_tag=se&keywords=lg%2Btv&nsdOptOutParam=true&qid=1744964176&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"},
    {"name": "lg tv", "price": "₹43,990", "store": "flipkart", "url": "https://www.flipkart.com/lg-lr57-80-cm-32-inch-hd-ready-led-smart-webos-tv-2025-alpha5-gen-6-ai-processor-100-free-channels-functions-hdr10-magic-remote-compatible-60hz-refresh-rate-satellite-connectivity-wi-fi-built-in/p/itmb61ea9903fd58?pid=TVSH9RMF8YPHSHA3&lid=LSTTVSH9RMF8YPHSHA3TJDN12&marketplace=FLIPKART&q=lg+tv&store=ckf%2Fczl&srno=s_1_1&otracker=search&otracker1=search&fm=search-autosuggest&iid=20678689-a5b5-42e1-90b1-eaaaedc2a424.TVSH9RMF8YPHSHA3.SEARCH&ppt=sp&ppn=sp&ssid=v5n72oaskg0000001744964112270&qH=0e9823883e72a0ba"},
    {"name": "fridge", "price": "₹17,490", "store": "Amazon", "url": "https://www.amazon.in/Samsung-Direct-Cool-Refrigerator-RR20D2825HV-NL/dp/B0CPPJ1NW3"},
    {"name": "fridge", "price": "₹16,390", "store": "flipkart", "url": "https://www.flipkart.com/whirlpool-184-l-direct-cool-single-door-2-star-refrigerator/p/itmc2bd80b306ecd?pid=RFRH99Z8ZGUGZS7T&lid=LSTRFRH99Z8ZGUGZS7TKCH3K7&marketplace=FLIPKART&q=fridge&store=j9e%2Fabm%2Fhzg&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&fm=organic&iid=en_WrsbXPJj51geqZsTGOwabSEubllvFL9XQhInLBFgjsUW421Uzwy-YqntFvNIFRiKE3fo53Zw6Ikn11Jmt6yNjA%3D%3D&ppt=hp&ppn=homepage&ssid=b29pozj4a80000001744620138393&qH=2be977f3ff92dd10"},
    {"name": "AC 1.5 Ton", "price": "₹31,490", "store": "Amazon", "url": "https://www.amazon.in/Godrej-Comprehensive-AC1-5T-18P3T-WZT/dp/B0DR327PJK/ref=sr_1_1_sspa?crid=7Q0PGKIPJ5J3&dib=eyJ2IjoiMSJ9.RvPkRvldR7USOZRaA7SpC3cVCdSZX3us00XUBiT5CyDoZus5F-3CHjG0tdZNzLkbFQuWRX0Hlcl4Dhvvggejy6ufnOlWlpn6smzBchomuuThA1DQJzIuybVOHW-IgSpEisbEFKMsunY5rBxP4VbXJvyOPK1adcnJVpatPL_0OI9HZLNDssAtT_tE-yBJI6EY3DuQzYSx6b_bgDUw3JxawuTYLIlKkxh4zuFZZhZd5Ig.W56-t4Dw-yfwLW-VKZVfmu39QnDUJTDlQEQHX7ZdP8E&dib_tag=se&keywords=ac%2B1.5%2Bton&qid=1744620517&sprefix=ac%2B1.5%2Bton%2Caps%2C201&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"},
    {"name": "AC 1.5 Ton", "price": "₹24,990", "store": "flipkart", "url": "https://www.flipkart.com/marq-flipkart-2025-1-5-ton-3-star-split-inverter-5-in-1-convertible-turbo-cool-technology-ac-white/p/itmfd8dfe14ce4f5?pid=ACNH76Z3W5YGCTSM&lid=LSTACNH76Z3W5YGCTSMCE9D2S&marketplace=FLIPKART&q=ac+1.5+ton&store=j9e%2Fabm%2Fc54&srno=s_1_3&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&fm=Search&iid=506aa801-84da-48f4-89c8-46970cbf61cc.ACNH76Z3W5YGCTSM.SEARCH&ppt=sp&ppn=sp&ssid=d0hy5burds0000001744620327150&qH=09362e2862616907"},
    {"name": "dishwasher", "price": "₹44,500", "store": "flipkart", "url": "https://www.flipkart.com/bosch-sms66gw01i-free-standing-13-place-settings-intensive-kadhai-cleaning-no-pre-rinse-required-dishwasher/p/itmfdzsgahybprgb?pid=DSWFDZSG7MCTU3GY&lid=LSTDSWFDZSG7MCTU3GYU21UYW&marketplace=FLIPKART&q=dishwasher&store=j9e%2Fm38%2F58n&spotlightTagId=default_FkPickId_j9e%2Fm38%2F58n&srno=s_1_6&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&fm=search-autosuggest&iid=91b2de18-20d8-45e5-a1f5-1ea5c82616ac.DSWFDZSG7MCTU3GY.SEARCH&ppt=sp&ppn=sp&ssid=xluztb59s00000001744620958650&qH=a1515828e3ab5803"},
    {"name": "dishwasher", "price": "₹47,500", "store": "Amazon", "url": "https://www.amazon.in/Bosch-Settings-Dishwasher-SMS66GI01I-Silver/dp/B07JW58P2C/ref=sr_1_2?crid=2ER165TU8MYNJ&dib=eyJ2IjoiMSJ9.-ElruQefHPqyOgrfxB60TUV2PYtnT4Q--pBmBDlsNlRgEX0Y_evcb9siT2XFfko-9iVjIka1K_oh_ZdcK1bh88ruFD1uP0kGCkH48FhdPmI512t98j965QW6ELtO_gxbKN9qE3LHgQ9L_Qgc48o1-xhjA_Bc-4P51z8EuaLIsP-liVMX3oz3Mm4GldW3cMVYG6LimpAX39GGc67xs31LiTKqeppOvo5fBY3JUe6iSjg.hB6qsyA53F3jhvbRes1cZckGXbqPOckGlPPgu95ANf8&dib_tag=se&keywords=dishwasher+machine&qid=1744620983&sprefix=di%2Caps%2C199&sr=8-2"},
    {"name": "whirlpool washing machine", "price": "₹17,990", "store": "Amazon", "url": "https://www.amazon.in/Whirlpool-7-5-SW-ROYAL-PLUS/dp/B0CMZKV2H1/ref=sr_1_1_sspa?crid=2HYGHLTMYJGLO&dib=eyJ2IjoiMSJ9.APmbvdbrJiY7RXtISha1WtxtauD7W4CL-jyDHaXwIDzYc7k0nlhTL_XfyyCQFv_zUY9lK2GhEIn7XP-ya6scvai9vaD5cBJEA4NJPKou_T7gulxTuZrR72X7z2Kou-XditZJKlR0iDtIYB5T7Yc_P-QEYrUT7jceXK1POFvaOWZFcEf6JCOg8sRSfDsGmPM1ZS6Im0IeRv9zN85okLxERfG-WAvI8Z1zORAT9pEhHhQ.QKJ5EwVHJDqAkOAw4dkVNhqhWwoXUW1tCg0bM0dW8nw&dib_tag=se&keywords=whirlpool%2Bwashing%2Bmachine%2B7kg&nsdOptOutParam=true&qid=1744622612&sprefix=Whirlpool%2Caps%2C199&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"},
    {"name": "whirlpool washing machine", "price": "₹9,290", "store": "flipkart", "url": "https://www.flipkart.com/whirlpool-6-5-kg-5-star-ace-wash-station-1400-rpm-speed-rust-proof-body-semi-automatic-top-load-washing-machine-grey/p/itm2d6d10af8a757?pid=WMNGVZF8G7XH4GZD&lid=LSTWMNGVZF8G7XH4GZDGNWQKU&marketplace=FLIPKART&q=whirlpool+washing+machine&store=j9e%2Fabm%2F8qx&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_2_9_na_na_ps&fm=Search&iid=en_2RcqFlUovV2I9mCkXApbZYkOjl-hABOQEl6OH5iCClJu63J54VmFGi6ncEE1v2R1tRkjmIyNyzNkUIXD3aEOhw%3D%3D&ppt=sp&ppn=sp&ssid=gelvrbdc280000001744622568846&qH=7b06f24fe9b4d7c2"},
    {"name": "whirlpool washing machine", "price": "$699.99", "store": "bestbuy", "url": "https://www.bestbuy.com/site/whirlpool-4-5-cu-ft-high-efficiency-front-load-washer-with-tumble-fresh-option-white/6585510.p?skuId=6585510"},
    {"name": "canon camera", "price": "₹33,390", "store": "flipkart", "url": "https://www.flipkart.com/canon-eos-3000d-dslr-camera-1-body-18-55-mm-lens/p/itm1f4ad2d1ba230?pid=CAMF3DHJURPEMNRN&lid=LSTCAMF3DHJURPEMNRNBKP0RG&marketplace=FLIPKART&q=digital+camera&store=jek%2Fp31&spotlightTagId=default_FkPickId_jek%2Fp31&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_na&fm=search-autosuggest&iid=f4e9a10b-57f5-487d-a923-a51b2272d740.CAMF3DHJURPEMNRN.SEARCH&ppt=sp&ppn=sp&ssid=ts1bx7pky80000001744623459723&qH=bb39f8ab3dc7d073"},
    {"name": "canon camera", "price": "₹33,690", "store": "Amazon", "url": "https://www.amazon.in/Canon-EOS-3000D-Digital-18-55mm/dp/B07BRWY6XV/ref=sr_1_1?crid=27VL4EML9KLS6&dib=eyJ2IjoiMSJ9.4HDeAwX5X9aU8zQJw9MaXG_hjWKuOQ16GHfS660nS4DgID-BTZcS3XMmftsvfsFZvhvFZOFOo9lo-2jB944opDb1Fr1REKXLTjxzug_t4mWV_uZR2wwr3pNsF6qEbbbf6cr7Et0wt1TMkAVVu0ig--ofUdQFwJgKoe5bYtXBPUTrriufLtvmu7RVOvk73iMKSi-VHmAd1QmH3ldnbwvows2POWNSQxkryC5dcA_SF6o.cHGrvC2XjYMlVYi9FRotKWjCE7qPsw1UDDfC5Pvluto&dib_tag=se&keywords=Canon+EOS+3000D+DSLR+Camera+1+Body%2C+18+-+55+mm+Lens+%28Black%29&nsdOptOutParam=true&qid=1744623550&sprefix=canon+eos+3000d+dslr+camera+1+body%2C+18+-+55+mm+lens+black+%2Caps%2C186&sr=8-1"},
    {"name": "canon camera", "price": "$479.99", "store": "bestbuy", "url": "https://www.bestbuy.com/site/canon-eos-rebel-t7-dslr-video-camera-with-18-55mm-lens-black/6323758.p?skuId=6323758"},
    {"name": "canon camera", "price": "₹40,900", "store": "LuLu Hypermart", "url": "https://www.luluhypermarket.in/product/electronic/canon-dslr-eos-1500d-kit-ef-s18-55-is-ii"}
]

# Insert products, avoiding duplicates by unique (store, description, price, link)
for p in products_to_add:
    c.execute('''
        INSERT OR IGNORE INTO products (store, total_results, description, price, link, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        p.get('store'),
        None,  # total_results not available
        p.get('name'),
        p.get('price'),
        p.get('url'),
        None   # image_url not available
    ))

# Fetch all products, ordered by product name (case-insensitive)
c.execute("SELECT description, store, link, price FROM products ORDER BY LOWER(description)")
products = c.fetchall()

# Count number of times each product appears (case-insensitive)
product_counts = Counter([p[0].lower() for p in products])

for description, store, link, price in products:
    total_for_product = product_counts[description.lower()]
    print(f"total results: {total_for_product}")
    print(f"product: {description}")
    print(f"store: {store}")
    print(f"price: {price}\n")

conn.commit()
conn.close()
print("Data stored in store.db!")