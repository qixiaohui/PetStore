import bs4 as bs
import urllib
import json
from postModel import db, Posts

for i in range(1, 51):
    src =urllib.urlopen('http://www.boredpanda.com/category/animals/page/'+str(i)+'/')
    soup = bs.BeautifulSoup(src, 'lxml')

    for article in soup.find_all('article'):
        pojo = {}
        title = article.find('a', {'class': 'title'})
        if title is None:
            continue
        pojo['title'] = title.text.strip()
        img = article.find('img', {'class': 'image-size-full'})
        if img is None:
            continue
        pojo['image'] = img['src'].strip()
        desc = article.find('p', {'class': 'description visible-downto-xs'})
        if desc is None:
            continue
        pojo['content'] = desc.text.strip()
        page = urllib.urlopen(title['href'])
        pageSoup = bs.BeautifulSoup(page, 'lxml')
        content = pageSoup.find('div', {'class': 'post-content'})
        if content is None:
            continue
        contentText = content.find_all('h3', recursive=False)
        contentImages = content.find_all('div', {'class': 'shareable-post-image'})
        imageList = []
        contentList = []
        for image in contentImages:
            if image is None:
                continue
            else:
                image = image.find('img')
                if image is None:
                    continue
                else:
                    imageSrc = image['src']
                    imageList.append(imageSrc)
        pojo['contentList'] = json.dumps(contentList)
        for content in contentText:
            if content is None:
                continue
            else:
                content = content.text
                contentList.append(content)
        pojo['imageList'] = json.dumps(imageList)
        print(json.dumps(pojo))
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')