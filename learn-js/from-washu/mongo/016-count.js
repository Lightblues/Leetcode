const {MongoClient} = require('mongodb');
// const uri = 'mongodb+srv://easonshi:eashonshi@cluster0.qzclh.mongodb.net/'
// const client = new MongoClient(uri)

const url = "mongodb+srv://easonshi:easonshi@cluster0.qzclh.mongodb.net/?writeConcern=majority";
const client = new MongoClient(url)

async function run() {
    try{
        await client.connect();
        const db = client.db("sample_mflix");
        const movies = db.collection('movies');

        let estimate = await movies.estimatedDocumentCount();   // 注意该函数不能传入参数
        console.log(`Estimated number of documents in the movies collection: ${estimate}`);
        estimate = await movies.countDocuments();
        console.log(`Actual number of documents in the movies collection: ${estimate}`);


        const quert = {countries: 'Canada'};
        let countCanada = await movies.countDocuments(quert);
        console.log(`Number of movies from Canada: ${countCanada}`);
    } finally {
        client.close();
    }
}

run().catch(console.dir)