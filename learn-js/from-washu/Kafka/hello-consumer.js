const kafka = require("kafka-node");

const client = new kafka.KafkaClient({kafkaHost: 'Jndroid-Kafka-01:9092'})
const topics = [
    {
        topic: 'webevents.dev'
    }
]
const options = {
    autoCommit: true,
    fetchMaxWaitMs: 1000,
    fetchMaxBytes: 1024 * 1024
    // encoding: 'buffer'
}
// { autoCommit: false, fetchMaxWaitMs: 1000, fetchMaxBytes: 1024 * 1024 };
const consumer = new kafka.Consumer(client, topics, options)
consumer.on('message', function (message) {
    // Read string into a buffer.
    console.info(`[message]:==:>${JSON.stringify(message)}`)
    const buf = new Buffer(String(message.value), 'binary')
    const decodedMessage = JSON.parse(buf.toString())
    console.log('decodedMessage: ', decodedMessage)
})
consumer.on('error', function (err) {
    console.log('error', err)
})
process.on('SIGINT', function () {
    consumer.close(true, function () {
        process.exit()
    })
})
