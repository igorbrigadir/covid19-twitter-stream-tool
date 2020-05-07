import os
import sys
import logging.handlers
import requests
import time
import subprocess


consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
partition = os.environ.get("PARTITION_ID")

if not consumer_key or not consumer_secret or not partition:
    print("WARNING: Consumer Keys and Partition number are not set!")
    sys.exit(0)


def namer(name):
    return f"{name}.jsonl"


def rotator(source, dest):
    print(f"Compressing {source} -> {dest}")
    try:
        os.rename(source, dest)
        subprocess.Popen(["xz", dest])
    except:
        print(f"WARNING: FAILED TO COMPRESS {dest}")


log_handler = logging.handlers.TimedRotatingFileHandler(
    f"/data/covid19_partition_{partition}",
    when="H",
    interval=1,
    encoding="utf-8",
    utc=True,
)
log_handler.rotator = rotator
log_handler.namer = namer

logger = logging.getLogger("covid19_logger_{}".format(partition))
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


def get_bearer_token(key, secret):
    response = requests.post(
        "https://api.twitter.com/oauth2/token",
        auth=(key, secret),
        data={"grant_type": "client_credentials"},
        headers={
            "User-Agent": "Python igorbrigadir/covid19-twitter-stream-tool v0.0.2"
        },
    )

    if response.status_code is not 200:
        raise Exception(
            f"Cannot get a Bearer token (HTTP %d): %s"
            % (response.status_code, response.text)
        )

    body = response.json()
    return body["access_token"]


def stream_connect(partition):
    response = requests.get(
        "https://api.twitter.com/labs/1/tweets/stream/covid19?partition={}".format(
            partition
        ),
        headers={
            "User-Agent": "Python igorbrigadir/covid19-twitter-stream-tool v0.0.2",
            "Authorization": "Bearer {}".format(
                get_bearer_token(consumer_key, consumer_secret)
            ),
        },
        stream=True,
    )
    for response_line in response.iter_lines():
        logger.info(response_line.decode("utf-8"))


def main():
    timeout = 0

    while True:
        print(f"Connecting to COVID-19 Stream Partition: {partition}")
        try:
            stream_connect(partition)
            time.sleep(2 ** timeout * 1000)
            timeout += 1
        except:
            pass
        print(
            f"WARNING: Disconnected Partition: {partition}, Attempt {timeout} to Reconnect"
        )

    sys.exit(1)


if __name__ == "__main__":
    main()
