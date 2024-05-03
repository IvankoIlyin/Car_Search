import logging
from bs4 import BeautifulSoup
import requests

logging.basicConfig(
    level='INFO',
    format='[%(levelname)-5s] %(asctime)s\t-\t%(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p'
)


def multiple_skip_to_content():

    # ### unique extractor
    url = 'https://www.wdbj7.com/2024/03/04/johnson-scores-21-points-virginia-beats-no-5-virginia-tech-after-star-kitley-leaves-with-injury/'
    response = requests.get(url)
    print(response.status_code)
    res = BeautifulSoup(response.content)




    not_allowed_keyword = ['Skip to content',
                           'Click here',
                           'click here',
                           'HERE',
                           'To learn more',
                           'Click Here',
                           'También te puede interesar',
                           'Derechos de autor',
                           'online here',
                           'MORE NEWS:',
                           'Watch continuous',
                           'Download the',
                           'it to us here',
                           'Subscribe to',
                           'For more details',
                           'To stay up to date ',
                           'Write us here',
                           'by clicking here',
                           'Refresh this page',
                           'Sign up for the',
                           'newsletter here',
                           'All rights reserved.']

    ## Title
    try:
        title = res.find('h1', class_='headline').text.strip().replace("\xa0", " ")
    except:
        title = None



    ## Content
    try:
        content1 = []
        content_div_p = res.find('div', class_='article-body').find_all('p')
        for i in content_div_p:
            if not any(keyword in i.text for keyword in not_allowed_keyword):
                content1.append(i.text)
        content = "\n".join(content1)
        content = content.replace("\xa0", " ")
    except:
        content = None

    ## Pub_date
    try:
        pub_date = res.find('span', attrs={'class': 'published-date-time'}).text.strip()

    except:
        try:
            pub_date = res.find('span', attrs={"class": "date-time"}).text.strip()
        except:
            pub_date = None

    try:
        pub_date = pub_date.replace("Published: ", "")
    except:
        None


    ## Author
    try:
        author = res.find('span', attrs={'class': 'author'}).text.strip()
    except:
        author = None

    ## Final res
    final = {"title": title, "content": content, "pub_date": pub_date, "author": author}
    #print(final)

    print("title:", title, '\n')
    print("content:",content, '\n')
    print("pub_date:",pub_date, '\n')
    print("author:",author, '\n')


multiple_skip_to_content()


