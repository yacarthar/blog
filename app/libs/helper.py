import re
from os.path import splitext

ALLOWED_EXTENSIONS = [".html"]


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


def allowed_file(filename):
    name, extension = splitext(filename)
    return extension in ALLOWED_EXTENSIONS
