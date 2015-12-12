from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.request, html5lib, re, bs4



def getHTML(url):
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as response:
        html = response.read()

    return html



def getLinksFromMainPage():


    def notBlogLink(href):
        return href and not re.compile("blog").search(href)

    def getPageLinkTags():
        ''' Get the <a> tags for links to the episode transcript pages. '''
        url = 'http://phtv.ifeng.com/program/qqsrx/'
        soup = BeautifulSoup(getHTML(url), 'html5lib')
        return soup.find_all("a", string=re.compile("详细"), href=notBlogLink)

    taglist = getPageLinkTags()
    urls = []
    for tag in taglist:
        urls.append(tag['href'])

    return urls


def getLinksFromEpisodePage(firstPage):
    soup = BeautifulSoup(getHTML(firstPage), 'html5lib')
    otherPageTags = soup.find_all("a", string=re.compile("^2$|^3$|^4$|^5$"))
    pageList = [ tag['href'] for tag in otherPageTags ]

    return pageList

def getUrlListForEpisode(firstPage):
    otherPagesList = getLinksFromEpisodePage(firstPage)
    return [firstPage] + otherPagesList



def getTextFromPage(url):

    def hasMainContentParent(tag):
        return (tag.find_parents(id="main_content") and 
                not tag.has_attr('style') and
                'p' in tag.name and
                not tag.name == 'a' and
                not tag.name == 'span' )


    soup = BeautifulSoup(getHTML(url), 'html5lib')
    results = soup.find_all(hasMainContentParent)

    bodyText = ""
    for tag in results:
        if tag.string:
            bodyText += tag.string +'\n'


    return bodyText



if __name__ == '__main__':
    currentEpisodes = getLinksFromMainPage()
    transcripts = []
    episodeCount = 1
    for episode in currentEpisodes:
        urllist = getUrlListForEpisode(episode)
        fullTranscript = ''
        for url in urllist:
            fullTranscript += getTextFromPage(url)
        print('======================================EPISODE' + str(episodeCount) + '=====================================================\n' +
                fullTranscript +
                '===========================================================================================')
        episodeCount += 1

