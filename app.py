import json

from urllib import request
from flask import Flask
from feedgen.feed import FeedGenerator

app = Flask(__name__)

base_url = 'http://zhuanlan.zhihu.com'
api = base_url + '/api/columns/%s/posts?limit=10'


@app.route('/favicon.ico')
def favicon():
    return '', 404


@app.route('/<string:column_id>', strict_slashes=False)
def feed(column_id):
    url = api % column_id
    with request.urlopen(url) as stream:
        result = stream.read().decode('utf-8')

    if not result:
        return '', 404

    entries = json.loads(result)
    with request.urlopen(base_url + entries[0]['href']) as stream:
        e = stream.read().decode('utf-8')
        e = json.loads(e)
        column_title = e['column']['name']

    fg = FeedGenerator()
    fg.id(str(entries[0]['slug']))
    fg.title(column_title)
    fg.language('zh_CN')
    fg.author(dict(name=column_title))
    fg.link(href='/'.join((base_url, column_id)), rel='alternate')
    for entry in entries:
        fe = fg.add_entry()
        fe.id(entry['url'])
        fe.title(entry['title'])
        fe.published(entry['publishedTime'])
        fe.updated(entry['publishedTime'])
        fe.author(dict(name=entry['author']['name']))
        fe.link(href='/'.join((base_url, entry['url'])), rel='alternate')
        fe.content(entry['content'])

    atom_feed = fg.atom_str(pretty=True)
    return atom_feed


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
