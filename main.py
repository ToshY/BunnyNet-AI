"""
@author: ToshY
"""

import hashlib
import argparse
import os
import sys
import logging as log
import shutil
import urllib.error
import urllib.parse
import urllib.request
from time import time, sleep
from base64 import b64encode
from slugify import slugify
from src.banner import cli_banner


def cli_args(args=None):
    """
    Command Line argument parser.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        required=True,
        help="API key for token authentication; e.g. '489eb71e-1259-4e1a-83c2-2d7859eec469'",
    )
    parser.add_argument(
        "-hn",
        "--hostname",
        type=str,
        required=True,
        help="Pull zone hostname; e.g. 'myzone.b-cdn.net'",
    )
    parser.add_argument(
        "-e",
        "--engine",
        type=str,
        required=False,
        default="dalle-1024",
        help="AI engine type; e.g 'dalle-1024'",
    )
    parser.add_argument(
        "-b",
        "--blueprint",
        type=str,
        required=False,
        default="default",
        help="Blueprint; e.g. 'default'",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        required=True,
        help="Search term to generate images; e.g. 'cute pixel art of a bunny with a colorful solid background'",
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        required=True,
        help="Amount of images to generate; e.g. '10'",
    )
    parser.add_argument(
        "-ext",
        "--extension",
        type=str,
        required=False,
        default="png",
        help="Image file extension; e.g. 'png'",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbose logging",
    )

    if args is not None:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    return args


# pylint: disable-next=too-many-arguments
def generate_secure_url(
    security_key: str,
    path: str,
    expire_timeframe: int = 120,
    host_name: str = str(),
    protocol: str = "https",
    filtered_ip: str = "",
) -> str:
    """
    Based on https://docs.bunny.net/docs/cdn-token-authentication-basic
    """
    expire_timestamp = int(time()) + expire_timeframe
    token_content = f"{security_key}{path}{expire_timestamp}{filtered_ip}"

    md5sum = hashlib.md5()
    md5sum.update(token_content.encode("ascii"))
    token_digest = md5sum.digest()
    token_base64 = b64encode(token_digest).decode("ascii")
    token_formatted = (
        token_base64.replace("\n", "")
        .replace("+", "-")
        .replace("/", "_")
        .replace("=", "")
    )

    return f"{protocol}://{host_name}{urllib.parse.quote(path)}?token={token_formatted}&expires={expire_timestamp}"


def download_helper(image_url: str, file_path: str, max_retries: int = 5) -> None:
    """
    Custom download helper for images with exponential retry in seconds.
    """
    request = urllib.request.Request(url=image_url)

    http_exception = ()
    retry_count = 0
    while 0 <= retry_count <= max_retries:
        log.info("Sending request `%s`", image_url)
        try:
            with urllib.request.urlopen(request) as response:
                with open(file_path, "wb") as save_file:
                    shutil.copyfileobj(response, save_file)

            log.info("Saved file to `%s`", file_path)
            return
        except urllib.error.HTTPError as response_exception:
            http_exception = response_exception
            if retry_count == max_retries:
                retry_count += 1
                continue

            sleep_time = pow(2, retry_count)
            retry_count += 1
            log.warning(
                "Error response when sending request: `%s`; Retrying after `%s` seconds...",
                http_exception,
                sleep_time,
            )
            sleep(sleep_time)

    if isinstance(http_exception, urllib.error.HTTPError):
        log.critical(
            "Unable to complete request for `%s` with response `%s`",
            image_url,
            http_exception,
        )


def main(custom_args=None) -> None:
    """
    Sending request to Bunny AI
    """
    input_args = cli_args(custom_args)
    file_extension = input_args.extension
    file_prompt = input_args.prompt
    slug_prompt = slugify(file_prompt)
    image_engine = input_args.engine
    image_blueprint = input_args.blueprint

    for _ in range(input_args.number):
        random_data = os.urandom(8)
        seed = int.from_bytes(random_data, byteorder="big")

        image_path = f"/.ai/img/{image_engine}/{image_blueprint}/{seed}/{slug_prompt}.{file_extension}"
        secure_url = generate_secure_url(
            input_args.key, image_path, 120, input_args.hostname
        )

        save_path = f"./output/[{image_blueprint}]{slug_prompt}-{seed}.{file_extension}"

        download_helper(secure_url, save_path)


if __name__ == "__main__":
    cli_banner("BunnyNet  AI")

    try:
        main()
    except KeyboardInterrupt:
        print("\r\n\r\n> [red]Execution cancelled by user[/red]")
        sys.exit()
