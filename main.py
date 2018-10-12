import os
import sys
import json
import argparse
from importlib import import_module

from extracter import Extracter
from converter import Converter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--measurement_type", default="d",
                        help="Type of measurement to tag (default = distance)")
    parser.add_argument("-t", "--text", help="Name of text file to tag")

    args = parser.parse_args()
    params = json.load(open("params.json", "r"))

    name = args.text
    text_dir = os.path.join(os.getcwd(), 'text')
    path = os.path.join(text_dir, name)

    try:
        m = params[args.measurement_type]
    except KeyError:
        print("Invalid measurement type!")
        sys.exit()

    cont_module = import_module("measurement.measures")
    cont_class = getattr(cont_module, m["container"])
    container = cont_class()
    converter = Converter(container)

    tag_module = import_module("tagger")
    tag_class = getattr(tag_module, m["tagger"])
    tagger = tag_class()

    format_module = import_module("formatter")
    format_class = getattr(format_module, m["formatter"])
    formatter = format_class()

    extracter = Extracter(path, tagger, formatter, converter)
    extracter.extract()
    print(extracter)


if __name__ == '__main__':
    main()
