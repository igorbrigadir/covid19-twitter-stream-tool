import os
import sys
import logging.handlers
import requests
import time
import subprocess


user_agent = "Python igorbrigadir/covid19-twitter-stream-tool v0.0.3"
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
stream_type = os.environ.get("STREAM_TYPE")
partition = os.environ.get("PARTITION_ID")


if not consumer_key or not consumer_secret or not partition or not stream_type:
    print("WARNING: Consumer Keys and Stream URL and Partition number are not set!")
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


folder = "compliance" if stream_type == "compliance" else "data"
log_handler = logging.handlers.TimedRotatingFileHandler(
    f"/{folder}/{stream_type}_partition_{partition}",
    when="H",
    interval=1,
    encoding="utf-8",
    utc=True,
)
log_handler.rotator = rotator
log_handler.namer = namer

logger = logging.getLogger(f"{stream_type}_logger_{partition}")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


def get_bearer_token(key, secret):
    response = requests.post(
        "https://api.twitter.com/oauth2/token",
        auth=(key, secret),
        data={"grant_type": "client_credentials"},
        headers={"User-Agent": user_agent},
    )

    if response.status_code is not 200:
        raise Exception(
            f"Cannot get a Bearer token (HTTP %d): %s"
            % (response.status_code, response.text)
        )

    body = response.json()
    return body["access_token"]


def stream_connect(partition):
    with requests.session() as s:
        s.keep_alive = False
        response = s.get(
            f"https://api.twitter.com/labs/1/tweets/stream/{stream_type}?partition={partition}",
            headers={
                "User-Agent": user_agent,
                "Connection": "close",
                "Authorization": f"Bearer {get_bearer_token(consumer_key, consumer_secret)}",
            },
            stream=True,
        )
        for response_line in response.iter_lines():
            logger.info(response_line.decode("utf-8"))


def main():
    retry = 0

    while True:
        print(f"Connecting to {stream_type} Stream Partition: {partition}")
        try:
            stream_connect(partition)
            wait_seconds = 2 ** retry
            time.sleep(wait_seconds if wait_seconds < 900 else 900)
            retry += 1
        except:
            pass
            print(
                f"WARNING: Disconnected {stream_type} Partition: {partition}, Attempt {retry} to Reconnect"
            )

    sys.exit(1)


if __name__ == "__main__":
    main()
