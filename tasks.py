from celery import Celery
from celery.schedules import crontab # scheduler

import requests # pulling data
from bs4 import BeautifulSoup # xml parsing
import json # exporting to files

app = Celery('tasks')

@app.task
def add(x, y):
    return x + y


# save function
def save_function(article_list):
    with open('articles.txt', 'w') as outfile:
        json.dump(article_list, outfile)

# scraping function
def hackernews_rss():
    article_list = []

    try:
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')

        # select only the "items" I want from the data
        articles = soup.findAll('item')

        # for each "item" I want, parse it into a list
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text

            # create an "article" object with the data
            # from each "item"
            article = {
                'title': title,
                'link': link,
                'published': published
                }

            # append my "article_list" with each "article" object
            article_list.append(article)
        
        # after the loop, dump my saved objects into a .txt file
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)


# scheduled task execution
# docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'tasks.<task here>',
        'schedule': crontab()
    },
    # executes every 15 minutes
    # 'scraping-task-fifteen-min': {
    #     'task': 'tasks.<task here>',
    #     'schedule': crontab(minute='*/15')
    # },
    # executes daily at midnight
    # 'scraping-task-midnight-daily': {
    #     'task': 'tasks.<task here>',
    #     'schedule': crontab(minute=0, hour=0)
    # }
}