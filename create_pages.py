'''
DO NOT EXECUTE THIS CODE.
THIS CODE WAS INITIALLY RAN TO GENERATE THE HTML FILES AND ADDS LINKS BETWEEN THEM.
'''

import wikipediaapi, os

def create_html_files(wiki_html):
    with open('words.txt', 'r') as file:
        for word in file.read().splitlines():
            with open('Pages/' + word + '.html', 'w') as file2:
                try:
                    file2.write(wiki_html.page(word).text)
                except:
                    file2.close()
                    os.remove('Pages/' + word + '.html')

def files():
    return [(fileName[0:len(fileName)-5]) for fileName in os.listdir("Pages")]

def get_possible_links(page):
    return [title for title in sorted(page.links.keys())]

def get_valid_links(page, wiki):
    valid_links = []
    for link in get_possible_links(wiki.page(page)):
        if link.lower() in files() and link.lower() != page:
            valid_links.append(link.lower())
    return valid_links

def add_links(page, links):
    with open('Pages/' + page + '.html', 'r') as file:
        fileData = file.read()
        for link in links:
            if link in fileData:
                fileData = fileData.replace(link, "<a href='"+ link +".html'>" + link + "</a>", 1)
    with open('Pages/' + page + '.html', 'w') as file:
        file.write(fileData)


wiki_html = wikipediaapi.Wikipedia(
	language='en',
	extract_format=wikipediaapi.ExtractFormat.HTML
)
wiki = wikipediaapi.Wikipedia('en')

for page in files():
    links = get_valid_links(page, wiki)
    add_links(page, links)
