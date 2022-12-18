"""
@author: ToshY
"""

import hashlib
import argparse
import os
import sys
import logging as log
from urllib.request import urlretrieve
from base64 import b64encode
from time import time
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
    security_key,
    path,
    expire_timeframe=120,
    host_name=str(),
    protocol="https",
    filtered_ip="",
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

    return f"{protocol}://{host_name}{path}?token={token_formatted}&expires={expire_timestamp}"


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

        log.info("Sending request `%s`", secure_url)
        urlretrieve(
            secure_url,
            f"./output/[{image_blueprint}]{slug_prompt}-{seed}.{file_extension}",
        )


if __name__ == "__main__":
    cli_banner("BunnyNet  AI")

    try:
        main()
    except KeyboardInterrupt:
        print("\r\n\r\n> [red]Execution cancelled by user[/red]")
        sys.exit()
