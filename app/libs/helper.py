import re


def clean_title(title):
    pattern = re.compile(r"[^\w\d\s]")
    cleaned_title = re.sub(pattern, "", title)
    return cleaned_title


def generate_link(title, post_id):
    title_ = clean_title(title)
    words = title_.split(" ")
    words.append(post_id)
    link = "/posts/" + "-".join(words)
    return link
