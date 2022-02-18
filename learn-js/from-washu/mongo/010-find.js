const {MongoClient} = require('mongodb')

// const url = "mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb";
const url = "mongodb+srv://easonshi:easonshi@cluster0.qzclh.mongodb.net/?writeConcern=majority";

const client = new MongoClient(url, {
    userNewUrlParser: true,
    useUnifiedTopology: true,
});
async function run() {
    try {
        await client.connect();
        const db = client.db('sample_mflix');
        const movies = db.collection('movies');

        /* findOne */
        // const query = {title: "The Room"};
        // // 和 shell 方式不同之处在于将 sort projection 等都放在了 options 参数中
        // const options = {
        //     sort: {rating: -1},
        //     projection: {_id: -1, imdb: 1}
        // };
        //
        // const movie = await movies.findOne(query, options);
        // console.log(movie);

        /* find */
        const query = {runtime: {$lt: 15}};
        const options = {
            sort: {tile: 1},
            projection: {_id: 0, title: 1, imdb: 1},
        };
        const cursor = movies.find(query, options);
        // 也可以链式 find, sort, projection
        // collection.find({ runtime: { $lt: 15 } }, { sort: { title: 1 }, projection: { _id: 0, title: 1, imdb: 1 }});
        // collection.find({ runtime: { $lt: 15 } }).sort({ title: 1}).project({ _id: 0, title: 1, imdb: 1 });
        if ((await cursor.count()) === 0){
            console.log("No document found");
        }
        await cursor.forEach(console.dir);
    } finally {
        await client.close();
    }
}

run().catch(console.dir);