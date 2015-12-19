import urllib.request
import re
from bs4 import BeautifulSoup


def get_html(url):
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        html = response.read()
    return html


class Page:

    url = None
    html = None
    soup = None
    body = ''
    heading = ''

    @classmethod
    def from_url(cls, url):
        return cls(url)

    def __init__(self, url):
        self.url = url
        self.html = get_html(url)
        self.soup = BeautifulSoup(self.html, 'html5lib')
        self.get_body()
        self.get_heading()

    def get_body(self):

        def has_main_content_parent(html_tag):
            return (html_tag.find_parents(id="main_content") and
                    not html_tag.has_attr('style') and
                    'p' in html_tag.name and
                    not html_tag.name == 'a' and
                    not html_tag.name == 'span')

        soup = BeautifulSoup(self.html, 'html5lib')
        results = soup.find_all(has_main_content_parent)
        for tag in results:
            if tag.string:
                self.body += tag.string + '\n\n'

    def get_heading(self):

        def has_article_topic_id(tag):
            return tag.has_attr('id') and tag['id'] == 'artical_topic'

        soup = BeautifulSoup(self.html, 'html5lib')
        results = soup.find_all(['h1', has_article_topic_id])
        results = list(results)
        self.heading = results[0].contents[0]
#  rewrite all into page class!!!


class Episode:

    @classmethod
    def from_first_page_url(cls, url):
        return cls(url)

    def __init__(self, url):
        self.pages = []
        self.title = ''
        self.transcript = ''
        self.get_first_page(url)
        self.get_remaining_pages()
        self.build_transcript()
        self.build_title()

    def get_first_page(self, first_url):
        assert(self.pages == [])
        first_p = Page.from_url(first_url)
        self.pages.append(first_p)

    def get_remaining_pages(self):
        remaining_pages_tags = self.first_page().soup.find_all("a", string=re.compile("^2$|^3$|^4$|^5$"))
        remaining_pages = [tag['href'] for tag in remaining_pages_tags]
        for link in remaining_pages:
            new_page = Page.from_url(link)
            self.pages.append(new_page)

    def build_transcript(self):
        for page in self.pages:
            self.transcript += str(page.body)

    def build_title(self):
        self.title = str(self.first_page().heading)

    def first_page(self):
        return self.pages[0]

    def __str__(self):
        return self.title + '\n\n' + self.transcript


class TranscriptFetcher:

    home_url = 'http://phtv.ifeng.com/program/qqsrx/'
    homepage_html = None
    episode_urls = []
    episodes = []

    def __init__(self):
        self.get_homepage_html()
        self.get_episode_urls()
        self.build_episodes_from_urls()

    def get_transcripts(self):
        return self.episodes

    def get_homepage_html(self):
        self.homepage_html = get_html(self.home_url)

    def get_episode_urls(self):

        def not_blog_link(href):
            return href and not re.compile("blog").search(href)

        def get_page_link_tags():
            """ Get the <a> tags for links to the episode transcript pages from the homepage. """
            self.homepage_soup = BeautifulSoup(self.homepage_html, 'html5lib')
            return self.homepage_soup.find_all("a", string=re.compile("详细"), href=not_blog_link)

        tag_list = get_page_link_tags()
        for tag in tag_list:
            self.episode_urls.append(tag['href'])

    def build_episodes_from_urls(self):
        for url in self.episode_urls:
            new_episode = Episode.from_first_page_url(url)
            self.episodes.append(new_episode)
