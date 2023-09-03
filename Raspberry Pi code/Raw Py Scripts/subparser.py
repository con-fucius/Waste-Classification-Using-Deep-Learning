from argparse import ArgumentParser

import argcomplete


class Garbage_parser:
    def add_take_photo_arguments(self, subparser):
        parser_take_photo = subparser.add_parser(
            "detect", help="detect an object"
        )
        parser_take_photo.add_argument("--button",
            action="store_true",
            dest="button",
            help="use button to control motors")

    def __init__(self) -> None:
        self._parser: ArgumentParser = ArgumentParser(
            prog="Garbage",
            usage="""""",
            description="CLI tool",
        )
        subparsers = self._parser.add_subparsers(dest="command")
        subparsers.add_parser("version", help="Check current version of Garbage.")
        self.add_take_photo_arguments(subparsers)
        argcomplete.autocomplete(self._parser)

    @property
    def parser(self):
        return self._parser
