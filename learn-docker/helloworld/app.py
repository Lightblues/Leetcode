from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
        count = redis.incr('hits')
        return 'Start page has been accessed {} times...'.format(count)
if __name__ == "__main__":
        app.run(host='localhost', debug=True)

