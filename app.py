import json

from urllib import request
from flask import Flask
from feedgen.feed import FeedGenerator

app = Flask(__name__)


class Api:
    base_url = 'http://zhuanlan.zhihu.com'
    base_api_url = base_url + '/api/columns'

    def __init__(self, column_id):
        self.column_id = column_id
        self.info = self.base_api_url + '/%s' % self.column_id
        self.posts = self.base_api_url + '/%s/posts?limit=10' % self.column_id


@app.route('/favicon.ico')
def favicon():
    return '', 404


@app.route('/<string:column_id>', strict_slashes=False)
def feed(column_id):
    api = Api(column_id)

    with request.urlopen(api.info) as stream:
        result = stream.read().decode('utf-8')

    if not result:
        return '', 404

    info = json.loads(result)

    with request.urlopen(api.posts) as stream:
        result = stream.read().decode('utf-8')
        entries = json.loads(result)

    fg = FeedGenerator()
    fg.id(str(entries[0]['slug']))
    fg.title(info['name'])
    fg.language('zh_CN')
    fg.icon(info['avatar']['template'].replace('{id}', info['avatar']['id']).replace('{size}', 's'))
    fg.logo(info['avatar']['template'].replace('{id}', info['avatar']['id']).replace('{size}', 'l'))
    fg.description(info['intro'])
    fg.author(dict(name=info['creator']['name']))
    fg.link(href=api.base_url + info['url'], rel='alternate')
    for entry in entries:
        fe = fg.add_entry()
        fe.id(entry['url'])
        fe.title(entry['title'])
        fe.published(entry['publishedTime'])
        fe.updated(entry['publishedTime'])
        fe.author(dict(name=entry['author']['name']))
        fe.link(href=api.base_url + entry['url'], rel='alternate')
        fe.content(entry['content'])

    rss_feed = fg.rss_str(pretty=True)
    return rss_feed


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
