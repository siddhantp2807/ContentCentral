from flask import Flask, render_template
from oop import Forbes, googleScraper, indianExpressScraper, indiaToday, bbcNews, nytimes, cnbc, reddit
app = Flask(__name__)

@app.route('/')
def homepage() :
    return render_template('index.html')

@app.route('/googleNews')
def googleNews() :
    google = googleScraper()
    data = google.newsLinks()
    section_data = {'World' : google.newsByTopic(), 'Science' : google.newsByTopic('experimentScience'), 'Sports' : google.newsByTopic('directions_bikeSports')}
    return render_template('news.html', data = data[0], domain = 'https://news.google.com/', name = 'Google News', sections = section_data)

@app.route('/indianExpress')
def indianExpress() :
    indExp = indianExpressScraper()
    data = indExp.indianExpress()
    section_data = {'World' : indExp.scrapeByUrl(url = 'https://indianexpress.com/section/world/'), 'Sports' : indExp.scrapeByUrl('https://indianexpress.com/section/sports/')[14:], 'Opinion' : indExp.scrapeByUrl('https://indianexpress.com/section/opinion/')[14:]}
    return render_template('news.html', data = data, domain = 'https://indianexpress.com/', name = 'The Indian Express', sections = section_data)

@app.route('/indiaToday')
def indToday() :
    ind = indiaToday()
    data = ind.parseLinks(url = 'https://www.indiatoday.in')
    section_data = {'Technology' : ind.parseLinks(url = 'https://www.indiatoday.in/technology'), 'Movies' : ind.parseLinks(url = 'https://www.indiatoday.in/movies'), 'Sports' : ind.parseLinks(url = 'https://www.indiatoday.in/sports')}
    return render_template('news.html', data = data, domain = 'https://www.indiatoday.in/', name = 'India Today', sections = section_data)

@app.route('/forbes')
def fbs() :
    forbes = Forbes()
    data = forbes.scrapeHomepage()
    section_data = {'Innovation' : forbes.scrapeByUrl(url = 'https://www.forbes.com/innovation/'), 'Business' : forbes.scrapeByUrl('https://www.forbes.com/business/'), 'Money' : forbes.scrapeByUrl('https://www.forbes.com/money/')}
    return render_template('news.html', data = data, domain = 'https://www.forbes.com/', name = 'Forbes', sections = section_data)

@app.route('/bbcNews')
def bbc() :
    news = bbcNews()
    data = news.scrapeHomePage()
    section_data = {'World' : news.scrapeByUrl(url = 'https://www.bbc.com/news/world'),'Science' : news.scrapeByUrl(url = 'https://www.bbc.com/news/science_and_environment'), 'Entertainment' : news.scrapeByUrl(url = 'https://www.bbc.com/news/entertainment_and_arts'), 'Tech' : news.scrapeByUrl(url = 'https://www.bbc.com/news/technology')}
    return render_template('news.html', data = data, domain = 'https://www.bbc.com/news', name = 'BBC News', sections = section_data)

@app.route('/nyTimes')
def nyt() :
    news = nytimes()
    data = news.scrapeWebpage()
    section_data = {"Today's Newspaper" : news.scrapeNewspaper(), 'Politics' : news.scrapeWebpage(url = 'https://www.nytimes.com/section/politics'), 'Health' : news.scrapeWebpage(url = 'https://www.nytimes.com/section/health')}
    return render_template('news.html', data = data, domain = 'https://www.nytimes.com/', name = 'The New York Times', sections = section_data)

@app.route('/cnbc')
def cb() :
    news = cnbc()
    data = news.scrapeHomepage()
    section_data = {'Business' : news.scrapeByUrl(url = 'https://www.cnbc.com/business/'), 'Investing' : news.scrapeByUrl(url = 'https://www.cnbc.com/investing/'), 'Tech' : news.scrapeByUrl(url = 'https://www.cnbc.com/technology/')}
    return render_template('news.html', data = data, domain = 'https://www.cnbc.com/', name = 'CNBC', sections = section_data)

@app.route('/reddit')
def rit() :
    redd = reddit()
    data = redd.parseRedditData()
    sections = {'memes' : redd.parseRedditData('memes'), 'AskReddit' : redd.parseRedditData('askreddit'), 'science' : redd.parseRedditData('science')}
    return render_template('reddit.html', data = data, sections = sections)

@app.errorhandler(404)
def error(e) :
    return render_template('error.html')

if __name__ == '__main__' :
    app.run(debug=True)













