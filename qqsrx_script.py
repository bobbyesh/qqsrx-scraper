import urllib.request
import re
from bs4 import BeautifulSoup


def get_html(url):
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        html = response.read()

    return html


def get_links_from_main_page():

    def not_blog_link(href):
        return href and not re.compile("blog").search(href)

    def get_page_link_tags():
        """ Get the <a> tags for links to the episode transcript pages. """
        url = 'http://phtv.ifeng.com/program/qqsrx/'
        soup = BeautifulSoup(get_html(url), 'html5lib')
        return soup.find_all("a", string=re.compile("详细"), href=not_blog_link)

    tag_list = get_page_link_tags()
    urls = []
    for tag in tag_list:
        urls.append(tag['href'])

    return urls


def get_links_from_episode_page(first_page):
    soup = BeautifulSoup(get_html(first_page), 'html5lib')
    other_page_pages = soup.find_all("a", string=re.compile("^2$|^3$|^4$|^5$"))
    page_list = [tag['href'] for tag in other_page_pages]
    return page_list


def get_url_list_for_episode(first_page):
    other_pages_list = get_links_from_episode_page(first_page)
    return [first_page] + other_pages_list


def get_text_from_page(url):

    def has_main_content_parent(html_tag):
        return (html_tag.find_parents(id="main_content") and
                not html_tag.has_attr('style') and
                'p' in html_tag.name and
                not html_tag.name == 'a' and
                not html_tag.name == 'span')

    soup = BeautifulSoup(get_html(url), 'html5lib')
    results = soup.find_all(has_main_content_parent)
    body_text = ""
    for tag in results:
        if tag.string:
            body_text += tag.string + '\n'

    return body_text


def build_transcript_from(episode_url):
    url_list = get_url_list_for_episode(episode_url)
    transcript = ''
    for link in url_list:
        transcript += get_text_from_page(link)
    return transcript


def get_current_transcripts():
    current_episodes = get_links_from_main_page()
    transcript_list = []
    for episode in current_episodes:
        transcript = build_transcript_from(episode)
        transcript_list.append(transcript)
    return transcript_list


if __name__ == '__main__':
    transcripts = get_current_transcripts()
