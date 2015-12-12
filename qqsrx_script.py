from bs4 import BeautifulSoup
import urllib.request, html5lib, re



def getHTML(url):
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        html = response.read()

    return html



def getTranscriptLinks():

    def notBlogLink(href):
        return href and not re.compile("blog").search(href)

    def getTranscriptPageLinkTags():
        ''' Get the <a> tags for links to the episode transcript pages. '''
        url = 'http://phtv.ifeng.com/program/qqsrx/'
        soup = BeautifulSoup(getHTML(url), 'html5lib')
        return soup.find_all("a", string=re.compile("详细"), href=notBlogLink)

    taglist = getTranscriptPageLinkTags()
    urls = []
    for tag in taglist:
        urls.append(tag['href'])

    return urls


def getTranscriptText(url):

    def getPages(url_):
        pass

    fullTranscript = ""
    for page in getPages(url):
        text = getBodyText(page)
        fullTranscipt += text

    return fullTranscript



if __name__ == '__main__':
    urls = getTranscriptLinks()
    transcripts = getTranscriptText(urls)
