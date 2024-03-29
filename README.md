**The COVID-19 Labs Stream Endpoint is now deprecated. In v2 API the alternative is to use `context:123.1220701888179359745` context annotation: https://developer.twitter.com/en/docs/twitter-api/annotations/overview**

# Twitter Labs COVID-19 Stream Tools

[![Labs](https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Flabs)](https://developer.twitter.com/en/docs/labs)

Get your Consumer Key and Consumer Secret from your app details in <https://developer.twitter.com/en/apps>

Enable the Labs **COVID-19 stream** and **Labs' compliance firehose stream** with your app on <https://developer.twitter.com/en/account/labs>

To start data gathering, run:

```bash
CONSUMER_KEY=xxx CONSUMER_SECRET=xxx docker-compose up -d
```

You need docker and docker compose already installed.

This will start a separate container for each stream partition, so that if one disconnects the rest will continue - hopefully this will minimise data loss. These will write separately into files, rotating and compressing every hour. This stream is roughly 8GB compressed per hour, but could be more, make sure you have disk space.

You will need to re-assemble the stream for further processing together with the compliance stream, which is separated into 8 partitions. Code for processing and applying this will be added [here](src/etl/README.md) later.

## See docker compose logs

Use `docker-compose logs -f -t` to *attach* yourself to the logs of *all running partitions*, Use `Ctrl + z` or `Ctrl + c` to *detach* yourself from the log output *without* shutting down your running containers. If you're interested in logs of a single container you can use the `docker` keyword instead: `docker logs -t -f <name-of-service>`

Tweets are saved in `/data` folder. You can change this in the docker-compose file if you want to mount somewhere else - this is where tweets will be written, in rotating hourly compressed `jsonl` files. Separately, if you also want to save the output of the docker compose logs to a file you can run: `docker-compose logs -f -t >> docker_compose_logs.log`.

## Other tools and links

Another alternative uses AWS: https://github.com/digitalepidemiologylab/covid-stream

If you have another one or questions, see the forum thread: https://twittercommunity.com/t/tools-for-consuming-covid-19-stream/137521
