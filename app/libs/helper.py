import re
from os.path import splitext
from urllib.parse import parse_qs, urlencode, urlparse

from flask import request

ALLOWED_EXTENSIONS = [".md", ".html"]


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


def build_url(page):
    parsed_url = urlparse(request.url)
    query_dict = parse_qs(parsed_url.query)
    query_dict["page"] = str(page)
    query_pairs = [(k, v) for k, vlist in query_dict.items() for v in vlist]
    query_string = urlencode(query_pairs)
    new_url = request.base_url + "?" + query_string
    return new_url
