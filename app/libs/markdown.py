import markdown
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag


def convert_to_html(markdown_content):
    return markdown.markdown(
        markdown_content, extensions=["fenced_code", "toc"]
    )


def extract_tag_body(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    if soup.body is not None:
        return str(soup.body)
    else:
        return html_text


def heading_level(h: Tag):
    heading_name = h.name
    return int(heading_name[-1])


def generate_ul_tag(headings: ResultSet, current_level):
    result = "<ul>"

    while headings and heading_level(headings[0]) == current_level:
        heading = headings.pop(0)
        result += f"\n  <li><a href='#{heading['id']}'>{heading.text}</a>"
        result += generate_ul_tag(headings, current_level + 1)
        result += "</li>"

    result += "\n</ul>"
    return result


def generate_toc(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    start_level = heading_level(headings[0])
    return generate_ul_tag(headings, start_level)
