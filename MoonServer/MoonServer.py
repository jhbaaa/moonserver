from flask import Flask, json, request, Response
import redis
from urllib import parse

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'


#curl -H "Content-type: application/json" -X GET http://127.0.0.1:5000/api/get_tops
#curl -H "Content-type: application/json" -X GET -i http://127.0.0.1:5000/api/get_tops
@app.route('/api/get_tops', methods=['GET'])
def api_get_tops():
    print('get_tops called')

    if request.method != 'GET':
        return ""
    
    if request.headers['Content-Type'] != 'application/json':
        return ""

    r = redis.Redis(db = 0)
    encoded_words = r.lrange("top20_words",0,20)
    
    words = []
    for encoded_word in encoded_words:
        word = encoded_word.decode("utf-8")
        words.append(word)
    
    print(words)

    data = {}
    for word in words:
        print(word)
        bcount = r.get(parse.quote(word))
        count = bcount.decode("utf-8")
        count = int(count)
        print(count)        
        data[word] = count
    
    print(data)

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://www.mooncle.com'

    return resp

if __name__ == '__main__':
    print('main called')
    app.run()
