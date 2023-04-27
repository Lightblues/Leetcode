// from <https://code.tutsplus.com/articles/understanding-the-magic-of-bloom-filters-with-nodejs-redis--cms-25397>

var Bloom = require('bloom-redis'),
    express = require('express'),
    redis = require('redis'),
    app,
    client,
    filter;

app = express();
client = redis.createClient();
filter = new Bloom.BloomFilter({
    client: client,
    key: 'username-bloom-filter',
    size: 2875518,
    numHashes: 20
})

app.get('/check', (req, res, next) => {
    if (typeof req.query.username === 'undefined') {
        next('route');
    } else {
        filter.contains(
            req.query.username,
            (err, result) => {
                if (err) {
                    next(err);
                } else {
                    res.send({
                        username: req.query.username,
                        status: result? 'used': 'free'
                    });
                }
            }
        );
    }
});

app.get('/save', function (req, res, next) {
    if(typeof req.query.username === 'undefined'){
        next('route');
    } else {
        filter.contains(req.query.username, function (err, result) {
            if (err) {next(err); } else {
                if (result) {res.send({
                    username: req.query.username,
                    status: 'not-created'});
                } else {
                    filter.add(
                        req.query.username, function (err) {
                            if (err) {next(err); } else {
                                res.send({
                                    username: req.query.username,
                                    status: 'created'
                                });
                            }
                        }
                    );
                }
            }
        });
    }
});

let port = 8010
app.listen(port);
console.log(`listening at http://localhost:${port}`)

