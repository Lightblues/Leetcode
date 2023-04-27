// const aaa =  require('mongodb');
// const MongoClient = aaa.MongoClient;

const { MongoClient } = require('mongodb');
// console.log(typeof MongoClient);
// process.exit();

const url = "mongodb+srv://easonshi:easonshi@cluster0.qzclh.mongodb.net/?writeConcern=majority";
const client = new MongoClient(url)

async function run() {
    try {

        await client.connect();
        const database = client.db('sample_mflix');
        const movies = database.collection('movies');

        /* insertOne */
        // const doc = {name: "Red", town: "kanto"};
        // const result = await movies.insertOne(doc);
        // console.log(`${result.insertedCount} documents ware inserted with the _id: ${result.insertedId}`);

        /* insertMany */
        const docs = [
            { name: "Red", town: "Kanto" },
            { name: "Blue", town: "Kanto" },
            { name: "Leon", town: "Galar" }
        ];
        const options = {ordered: true};
        const result = await movies.insertMany(docs, options);
        console.log(`${result.insertedCount} documents ware inserted`);
    } finally {
        await client.close();
    }
}
run().catch(console.dir);