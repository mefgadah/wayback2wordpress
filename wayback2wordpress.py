import requests
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import json,time
from datetime import datetime



# Step 1: Extract blog_ids from Internet Archive JSON
blog_ids = set()
if False:
    archive_url = f"https://web.archive.org/web/timemap/json?url={youroldurl.com}&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=10000&_=1703940417831"

    response = requests.get(archive_url)
    archive_data = response.json()

    

    for item in archive_data:
        url = item[0]
        if "/archives/" in url or "?p=" in url:
            blog_id = url.split("/")[-1].split("?p=")[-1]
            if blog_id.isdigit():
                blog_ids.add(int(blog_id))

    # Save blog_ids to old2new.json
    old2new_mapping = {blog_id: 0 for blog_id in blog_ids}
    with open("old2new.json", "w") as json_file:
        json.dump(old2new_mapping, json_file)
else:
    # Load old2new.json
    with open("old2new.json", "r") as json_file:
        old2new_mapping = json.load(json_file)

    # Get blog_ids with values equal to 0
    blog_ids = [blog_id for blog_id, new_post_id in old2new_mapping.items() if new_post_id == 0]


# Step 2: Access individual blog pages on Internet Archive

wp_url = "http://youroldurl.com/archives/{}"

for blog_id in blog_ids:
    archive_page_url = f"http://web.archive.org/web/{wp_url.format(blog_id)}"
    archive_page_response = requests.get(archive_page_url)
    print(archive_page_url)
   

    # Step 3: Parse the content using BeautifulSoup
    soup = BeautifulSoup(archive_page_response.content, "html.parser")

    # Step 4: Extract title, date, and content
    title = ""
    date = ""
    content = ""

    # First possible case
    entry_title = soup.find(class_="entry-title")
    published_date = soup.find(class_="published")
    entry_content = soup.find(class_="entry-content")

    # Second possible case
    if entry_title and published_date and entry_content:
        title = entry_title.text.strip()
        date_str = published_date.text.strip()
        content = entry_content.decode_contents()
        date_str = date_str.replace("下午", "PM").replace("上午", "AM")
        date = datetime.strptime(date_str, "%Y 年 %m 月 %d 日 at %p %I:%M")
        date = date.strftime("%a, %d %b %Y %H:%M:%S +0000")
    # Third possible case
    else:
        corner_title = soup.find("a", class_="corner")
        # edit_date = soup.find("div", class_="edit").find("li")
        edit_date = datetime.now()
        date = edit_date.strftime("%a, %d %b %Y %H:%M:%S +0000")
        post_content = soup.find("div", id="post")

        if corner_title and edit_date and post_content:
            title = corner_title.text.strip()
            # date = edit_date.text.strip().split(" - ")[0]
            content = post_content.decode_contents()

    # Convert date format if necessary (implement your own conversion logic)
    # ...
    print(title,date)
    # Step 5: Post to new WordPress site using wordpress_xmlrpc
    if title and date and content:
        wp = Client('https://yourblog.wordpress.com/xmlrpc.php', 'name', 'password')

        post = WordPressPost()
        post.title = title
        post.content = content
        post.date = date

        new_post_id = wp.call(NewPost(post))
        old2new_mapping[blog_id] = new_post_id

        # Update old2new.json with new_post_id values
        with open("old2new.json", "w") as json_file:
            json.dump(old2new_mapping, json_file)
    time.sleep(60)