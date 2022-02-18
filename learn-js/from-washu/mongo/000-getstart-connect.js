// from <https://docs.atlas.mongodb.com/tutorial/insert-data-into-your-cluster/>


// const MongoClient = require('mongodb').MongoClient;
// const uri = "mongodb+srv://easonshi:easonshi@cluster0.qzclh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";
// const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
// client.connect(err => {
//     const collection = client.db("test").collection("devices");
//     console.log(collection);
//     // perform actions on the collection object
//     client.close();
// });

const {MongoClient} = require('mongodb');

// Atlas 地址
// const url = "mongodb+srv://easonshi:easonshi@cluster0.qzclh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";
const url = "mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb";
const client = new MongoClient(url);

const dbName = "myproject",
    colName = "people";

async function run() {
    try {
        await client.connect();
        console.log("Connected to the server. ");
        const db = client.db(dbName);
        const col = db.collection(colName);

        // // Construct a document
        // let personDocument = {
        //     "name": {
        //         "first": "Eason",
        //         "last": "Shi"
        //     },
        //     "birth": new Date(1912, 5, 23), // June 23, 1912
        //     "death": new Date(1954, 5, 7),  // June 7, 1954
        //     "contribs": [ "Turing machine", "Turing test", "Turingery" ],
        //     "views": 1250000
        // }
        // // Insert a single document, wait for promise so we can read it back
        // const p = await col.insertOne(personDocument);

        // Find one document
        // const myDoc = await col.findOne();
        const myDoc = await col.find().toArray();       // 或者用 find，注意其返回的是一个 Cursor，参 http://mongodb.github.io/node-mongodb-native/3.6/api/Cursor.html#toArray
        // Print to the console
        console.log(myDoc);

    } catch (err) {
        console.log(err.stack);
    } finally {
        await client.close();
    }
}

// 注意对 Promise 的处理
run().catch(console.dir);