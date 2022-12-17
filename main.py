"""
@author: ToshY
"""

import hashlib
import argparse
import os
from urllib.request import urlretrieve
from base64 import b64encode
from src.banner import cli_banner
from time import time
from loguru import logger
from slugify import slugify


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
        help="API key for token authentication; e.g. 489eb71e-1259-4e1a-83c2-2d7859eec469",
    )
    parser.add_argument(
        "-hn",
        "--hostname",
        type=str,
        required=True,
        help="Pull zone hostname; e.g. myzone.b-cdn.net",
    )
    parser.add_argument(
        "-e",
        "--engine",
        type=str,
        required=False,
        default="dalle-1024",
        help="AI engine type; e.g dalle-1024",
    )
    parser.add_argument(
        "-b",
        "--blueprint",
        type=str,
        required=False,
        default="default",
        help="Blueprint; e.g. default",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        required=True,
        help="Search term to generate images; e.g. cats",
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        required=True,
        help="Amount of images to generate; e.g. 10",
    )
    parser.add_argument(
        "-ext",
        "--extension",
        type=str,
        required=False,
        default="png",
        help="Image file extension; e.g. png",
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

    return args


def generate_secure_url(
    security_key, path, expire_timeframe=120, base_url=str(), filtered_ip=""
) -> object:
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

    return f"{base_url}{path}?token={token_formatted}&expires={expire_timestamp}"


@logger.catch
def main(custom_args=None):
    input_args = cli_args(custom_args)

    for _ in range(input_args.number):
        random_data = os.urandom(8)
        seed = int.from_bytes(random_data, byteorder="big")

        ai_url = (
            f"https://{input_args.hostname}/.ai/img/{input_args.engine}/{input_args.blueprint}/{seed}/"
            f"{input_args.prompt}.{input_args.extension}"
        )
        file_name = f"{slugify(input_args.prompt)}-{seed}"

        urlretrieve(ai_url, f"./output/{file_name}")


if __name__ == "__main__":
    """Main"""
    cli_banner("BunnyNet  AI")

    try:
        main_result = main()
    except KeyboardInterrupt:
        print("\r\n\r\n> [red]Execution cancelled by user[/red]")
        exit()
