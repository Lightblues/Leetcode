const {MongoClient} = require('mongodb');
// const uri = 'mongodb+srv://easonshi:eashonshi@cluster0.qzclh.mongodb.net/'
// const client = new MongoClient(uri)

const url = "mongodb+srv://easonshi:easonshi@cluster0.qzclh.mongodb.net/?writeConcern=majority";
const client = new MongoClient(url)

async function run() {
    try {
        await client.connect();
        const database = client.db('sample_mflix');
        const movies = database.collection('movies');


        /* updateOne */
        // const filter = { title: "Blacksmith Scene" };
        // const options = {upsert: true};     // 查询不到的话插入
        // const updateDoc = {
        //     $set: {
        //         plot: "Blacksmith Scene is a silent film directed by William K.L. Dickson",
        //     }
        // };
        // const result = await movies.updateOne(filter, updateDoc);
        // console.log(`${result.matchedCount} document(s) matched the filter, updated ${result.modifiedCount} document(s)`);


        /* updateMany */
        const filter = {rated: 'G'};
        const updateDoc = {
            $inc: {
             num_mfix_comments: 2,
            }
        };
        const result = await movies.updateMany(filter, updateDoc);
        console.log(result);

        const res = await movies.find(filter).toArray();
        console.log(res);
    } catch (err) {
        console.log(err);
    } finally {
        client.close();
    }
}

run().catch(console.dir);