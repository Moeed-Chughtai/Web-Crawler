from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

class Pages:
    def __init__(self, name):
        self.name = name
        self.outgoingLinks = 0
        self.incomingPages = []
        self.pageRank = 1
        self.occurrence = 0

def incoming_links():
    pages = []
    for page in os.listdir('Website/Pages'):
        pages.append(Pages(page))
        links = []
        with open(os.path.join('Website/Pages', page)) as f:
            content = f.read()
            soup = BeautifulSoup(content, features='html.parser')
            for a in soup.find_all('a', href=True):
                links.append(a['href'])
        for link in links:
            for position, webPage in enumerate(pages):
                if link == webPage.name:
                    pages[position].incomingPages.append(page)
    return pages

def outgoingLinks(pages):
    for page in pages:
        page.outgoingLinks = len(page.incomingPages)

def page_rank_algorithm(page, pages):
    dampingFactor = 0.85
    shareRank = 0
    if len(page.incomingPages) == 0:
        page.pageRank = 1 - dampingFactor
    else:
        for i in range(len(page.incomingPages)):
            for webPage in pages:
                if webPage.name == page.incomingPages[i]:
                    shareRank += webPage.pageRank / page.outgoingLinks
        page.pageRank = (1 - dampingFactor) + (dampingFactor * shareRank)

def page_rank(pages):
    for i in range(35):
        for page in pages:
            page_rank_algorithm(page, pages)

def search_term(pages, query):
    rankedPages = {}
    if query:
        for page in pages:
            with open(os.path.join('Website/Pages', page.name)) as f:
                page.occurrence = f.read().lower().count(query.lower())
            if page.occurrence > 0:
                rankedPages[page] = page.occurrence * page.pageRank
        rankedPages = sorted(rankedPages.items(), key=lambda x: x[1], reverse=True)[:5]
    return rankedPages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('search_input', '')
        return redirect(url_for('search_results', query=query))
    return render_template('index.html')

@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        query = request.form.get('search_input', '')
        if not query:
            return "No search query provided"
        pages = incoming_links()
        outgoingLinks(pages)
        page_rank(pages)
        rankedPages = search_term(pages, query)
        return render_template('search_results.html', rankedPages=rankedPages)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
