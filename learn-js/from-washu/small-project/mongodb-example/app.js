/*
来自一个老版本的教程 <http://mongodb.github.io/node-mongodb-native/3.4/quick-start/quick-start/>
 */
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const url = 'mongodb://localhost:27017';
const dbName = 'myproject';

const client = new MongoClient(url, {useNewUrlParser: true});

// client.connect(fu)

client.connect(function(err) {
    assert.equal(null, err);
    console.log("Connected successfully to server");

    const db = client.db(dbName);
    updateDocuments(db, function (){
        removeDocument(db, function (){
            findDocuments(db, function (){
                indexCollection(db, function (){
                    client.close();
                });
            });
        });

    });
    // insertDocuments(db, function (){
    //     findDocuments(db, function (){
    //         client.close();
    //     })
    // });

    // client.close();
});
// .catch(err => {
//     console.log(err);
// });

const insertDocuments = function (db, callback) {
    const collection =  db.collection('documents');
    collection.insertMany([
        {a:1}, {a:2}, {a:3}
    ], function (err, result) {
        assert.equal(err, null);
        assert.equal(3, result.result.n);
        assert.equal(3, result.ops.length);
        console.log("Inserted 3 documents into the collection");
        callback(result);
    })
}

const findDocuments = function (db, callback) {
    const collection = db.collection('documents');
    collection.find({}).toArray(function (err, docs){
        assert.equal(err, null);
        console.log("Found the following records");
        console.log(docs);
        callback(docs);
    });
}

const updateDocuments = function (db, callback){
    const collection = db.collection('documents');
    collection.updateOne(
        {a:2},
        {$set: {b:1}},
        function (err, result) {
            assert.equal(err, null);
            assert.equal(result.result.n, 1);
            console.log("Updated the document with the field a equal to 2");
            callback(result);
        }
    )
}

const removeDocument = function (db, callback){
    const collection = db.collection("documents");
    collection.deleteOne({a:3}, function (err, result){
        assert.equal(err, null);
        assert.equal(result.result.n, 1);
        console.log("Removed the document with the field a equal to 3");
        callback(result);
    })
}

const indexCollection = function (db, callback){
    db.collection('documents').createIndex(
        {'a':1},
        null,
        function (err, results){
            console.log(results);
            callback(results);
        }
    )
}