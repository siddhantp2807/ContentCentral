import urllib.request, urllib.error, urllib.parse
import ssl
from bs4 import BeautifulSoup
import re
import requests

class googleScraper() :
    def __init__(self) :
        pass
    
    def scrapeallLinks(self, url = 'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN%3Aen') :
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False 
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(url, context= ctx)
        
        bs = BeautifulSoup(html.read(), 'html.parser')
        
        links_with_text = [{ 'href' : a['href'], 'text' : a.text} for a in bs.find_all('a', href=True) if a.text]

        return links_with_text
        
    def newsLinks(self, url = 'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN%3Aen') :
        articleLink = re.compile(r'^(./articles/)')
        topicLink = re.compile(r'^(./topics/)')
        articles, topics = [], []
        x = self.scrapeallLinks(url)
        for i in x :
            if articleLink.findall(i['href']):
                articles.append(i)
            if topicLink.findall(i['href']) :
                topics.append(i)
        return [{ 'href' : 'https://news.google.com/' + i['href'], 'text' : i['text']} for i in articles], [{ 'href' : 'https://news.google.com/' + i['href'], 'text' : i['text']} for i in topics]

    def newsByTopic(self, topic = 'publicWorld') :
        topicUrls = self.newsLinks()[1]
        
        for top in topicUrls :
            if top['text'] == topic :
                return self.newsLinks(url = top['href'])[0]
        return []
    
class indianExpressScraper() :
    def __init__(self) :
        pass

    def indianExpress(self, url = 'https://indianexpress.com/') :
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        html = urllib.request.urlopen(url, context = ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')
        #For Top news
        findArticles = bSoup.find('div', {'class' : 'top-news'}).find_all('a', recursive = True)
        otherArticles = bSoup.find_all('div', {'class' : 'other-article'})
        oArts = []
        for j in otherArticles :
            for k in j.find_all('a', recursive = True) :
                oArts.append(k)
        articles = []
        for art in findArticles :
            if art.text : 
                articles.append({'href' : art.attrs['href'], 'text' : art.text})
        for article in oArts :
            if article.text :
                articles.append({'href' : article.attrs['href'], 'text' : article.text})
        
        return articles
    def getTopics(self) :
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE    

        html = urllib.request.urlopen('https://indianexpress.com/', context = ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')
        
        return [{ 'href' : i['href'], 'text' : i.text }for i in bSoup.find('div', {'class' : 'mainnav'}).find_all('a', recursive = True)]
    
    def scrapeByUrl(self, url) :
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE    
        isArticle = re.compile(r'^https://indianexpress.com/article')
        
        html = urllib.request.urlopen(url, context = ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')

        articles = [{'text' : i.text, 'href': i.attrs['href'] } for i in bSoup.find_all('a') if isArticle.findall(i['href']) and i.text]
        return articles        

class indiaToday() :
    def __init__(self) :
        pass

    def indiaToday(self, url = 'https://www.indiatoday.in/' ) :
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(url, context= ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')
        found_links = [{'href' : i.attrs['href'], 'text' : i.text} for i in bSoup.find_all('a') if 'href' in i.attrs.keys() and i.text]

        return found_links

    def parseLinks(self, url) :
        islink = re.compile(r'^(/[a-zA-Z0-9]+)(/)')
        validEnd = re.compile(r'([0-9]{4}-[0-9]{2}-[0-9]{2})$')
        allLinks = self.indiaToday(url)
        
        fullyParsed = [{'href' : 'https://www.indiatoday.in' + el['href'], 'text' : el['text']} for el in allLinks if islink.findall(el['href']) and validEnd.findall(el['href'])]
        return fullyParsed


class Forbes() :
    def __init__(self, homePage = 'https://www.forbes.com/') :
        self.homePage = homePage
        pass
    def scrapeHomepage(self) :
        url = self.homePage
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(url, context=ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')

        headlink = [{ 'href' : link.attrs['href'], 'text' : link.text} for link in bSoup.find_all('a', {'class' : 'headlink'})] 
        
        breakingNews = [{ 'href' : link.attrs['href'], 'text' : link.text} for link in bSoup.find_all('a', {'class' : 'happening__title'}) if link.text and 'href' in link.attrs.keys()] 
        
        return headlink + breakingNews

    def scrapeByUrl(self, url = 'https://www.forbes.com') :
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(url, context=ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')
        headlinks = [{'href' : i.attrs['href'], 'text' : i.text} for i in bSoup.find_all('a', {'class' : 'headlink'})]

        return headlinks




class bbcNews() :
    def __init__(self, homePage = 'https://www.bbc.com/news') :
        self.homePage = homePage
    def scrapeHomePage(self) :
        matchStart = re.compile(r'^/news')
        matchEnd = re.compile(r'.*-([0-9]){8}$')
        url = self.homePage
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(url, context=ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')
        allLinks = [{'href' : 'https://www.bbc.com' + i.attrs['href'], 'text' : i.text} for i in bSoup.find_all('a') if i.text and matchEnd.findall(i.attrs['href']) and matchStart.findall(i.attrs['href'])]

        return allLinks[6:-5]
    def scrapeByUrl(self, url = 'https://www.bbc.com/news') :
        matchStart = re.compile(r'^/news')
        matchEnd = re.compile(r'.*-([0-9]){8}$')
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen(url, context=ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')
        allLinks = [{'href' : 'https://www.bbc.com' + i.attrs['href'], 'text' : i.text} for i in bSoup.find_all('a') if i.text and 'href' in i.attrs and matchEnd.findall(i.attrs['href']) and matchStart.findall(i.attrs['href']) and i.text != 'Read morenext']
        
        distinctLinks = list(set([(i['href'], i['text']) for i in allLinks]))
        
        newLinks = [{'href' : distinctLinks[i][0], 'text' : distinctLinks[i][1]} for i in range(len(distinctLinks))]


        return newLinks[5:]


class nytimes() :
    def __init__(self, urlHomePage = 'https://www.nytimes.com/international/') :
        self.urlHomePage = urlHomePage
    
    def scrapeWebpage(self, url = 'https://www.nytimes.com/international/') :
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        isSpam = re.compile(r'[\n]{3,}')
        isDate = re.compile(r'/[0-9]{4}/[0-1][0-9]/[0-3][0-9]{1}/')
        html = urllib.request.urlopen(url, context = ctx)
        bSoup = BeautifulSoup(html.read(), 'html.parser')
        allLinks = [{'href' : 'https://nytimes.com' + i['href'], 'text' : i.text} for i in bSoup.find_all('a') if i.text and isDate.findall(i['href']) and not isSpam.findall(i.text)]
        return allLinks

    def scrapeNewspaper(self) :
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urllib.request.urlopen('https://www.nytimes.com/section/todayspaper', context=ctx)
        isDate = re.compile(r'^/[0-9]{4}/[0-1][0-9]/[0-3][0-9]{1}/')
        bSoup = BeautifulSoup(html.read(), 'html.parser')
        articles = [{'href' : link.attrs['href'], 'text' : link.text} for link in bSoup.find_all('a') if link.text and isDate.findall(link.attrs['href'])]

        for i in articles :
            if 'https://nytimes.com' in i['href'] :
                i['href'] = i['href']
            else :
                i['href'] = 'https://www.nytimes.com' + i['href']
        
        return articles

class cnbc() :
    def __init__(self, homePage = 'https://www.cnbc.com/') :
        self.homePage = homePage
    def scrapeHomepage(self) :
        url = self.homePage
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        html = urllib.request.urlopen(url, context=ctx)
        isDated = re.compile(r'^https://www.cnbc.com/[0-9]{4}/[0-1][0-9]/[0-3][0-9]')

        bSoup = BeautifulSoup(html.read(), 'html.parser')
        articles = [{'href' : link.attrs['href'], 'text' : link.text} for link in bSoup.find_all('a') if isDated.findall(link.attrs['href'])]

        return articles
    def scrapeByUrl(self, url) :
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        html = urllib.request.urlopen(url, context=ctx)

        bSoup = BeautifulSoup(html.read(), 'html.parser')
        isDated = re.compile(r'^https://www.cnbc.com/[0-9]{4}/[0-1][0-9]/[0-3][0-9]')
        articles = [{'href' : link.attrs['href'], 'text' : link.text} for link in bSoup.find_all('a', {'class' : 'Card-title'}) if link.text and isDated.findall(link.attrs['href'])]

        return articles

class reddit() :
    def __init__(self, homePage = 'https://www.reddit.com/.json?limit=25') :
        self.homePage = homePage

    def scrapeTopRedditFeed(self) :
        header = {'User-agent' : 'Content-Central-Bot'}
        data = requests.get(self.homePage, headers = header)
        return data.json()

    def scrapeSubredditData(self, subreddit) :
        header = {'User-agent' : 'Content-Central-Bot'}
        if subreddit == '' :
            data = requests.get(f'https://www.reddit.com/.json?limit=40', headers = header) 
        else :
            data = requests.get(f'https://www.reddit.com/r/{subreddit}/.json?limit=22', headers = header)
        finalData = data.json()

        return finalData
    
    def parseRedditData(self, subreddit = '') :

        data = self.scrapeSubredditData(subreddit) if subreddit else self.scrapeTopRedditFeed()

        fnlData = []

        for i in range(2, len(data['data']['children']), 1) :
            if ('post_hint' in data['data']['children'][i]['data']) :
                if (data['data']['children'][i]['data']['post_hint'] == 'image') :
                    fnlData.append({'url' : 'https://www.reddit.com'+data['data']['children'][i]['data']['permalink'], 'imgUrl' : data['data']['children'][i]['data']['url_overridden_by_dest'], 'title' : data['data']['children'][i]['data']['title'], 'author' : data['data']['children'][i]['data']['author'], 'subreddit' : data['data']['children'][i]['data']['subreddit'],  'subredditUrl' : 'https://www.reddit.com/r/'+ data['data']['children'][i]['data']['subreddit']})
            else :
                fnlData.append({'url' : data['data']['children'][i]['data']['url'], 'imgUrl' : '', 'title' : data['data']['children'][i]['data']['title'], 'author' : data['data']['children'][i]['data']['author'], 'subreddit' : data['data']['children'][i]['data']['subreddit'], 'subredditUrl' : 'https://www.reddit.com/r/'+ data['data']['children'][i]['data']['subreddit']})
        
        return fnlData
