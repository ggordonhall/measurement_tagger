"""Main logic"""

import os
import sys
import json
import argparse

from modules.tagger import Tagger
from modules.converter import Converter
from modules.extractor import Extractor

from modules.utils import join
from modules.utils import hyponyms
from modules.utils import get_class


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--measurement_type", default="d", choices=["d", "t", "m", "e", "v"],
                        help="Type of measurement to tag (default = distance)")
    parser.add_argument(
        "-t", "--text", help="Name of text file to tag (required)", required=True)
    parser.add_argument("--max_gram", type=int, default=2,
                        help="The maximum n-gram measurement unit to tag (default = 2)")
    parser.add_argument("--return_unconverted", action="store_true",
                        help="Return measurements that have not been normalised")
    parser.add_argument("--parallel", action="store_true",
                        help="Flag to run the tokeniser on the multiple cores")
    parser.add_argument("--batch_size", default=1000, type=int,
                        help="The number of sentences to pass to each tokeniser subprocess (default = 1000)")
    parser.add_argument("--n_jobs", default=3, type=int,
                        help="The number of cores (default = 3)")

    args = parser.parse_args()
    params_path = os.path.join(os.getcwd(), "modules/params.json")
    params = json.load(open(params_path, "r"))

    name = args.text
    text_dir = os.path.join(os.getcwd(), "text")
    path = os.path.join(text_dir, name)

    try:
        m = params[args.measurement_type]
    except KeyError:
        print("Invalid measurement type!")
        sys.exit()

    container = get_class("measurement.measures", m["container"])
    formatter = get_class("modules.formatter", m["formatter"])
    converter = Converter(container, args.return_unconverted)

    tags = m["tags"]
    if not tags:
        tags = hyponyms(m["synset"])
        params[args.measurement_type]["tags"] = list(tags)
        json.dump(params, open(params_path, "w"))
    tagger = Tagger(tags, args.max_gram, m["right_mods"])

    if args.parallel:
        extractor = Extractor(path, tagger, formatter,
                              converter, (args.batch_size, args.n_jobs))
    else:
        extractor = Extractor(path, tagger, formatter, converter)

    for measure in extractor.extract():
        print(join(measure) if isinstance(measure, tuple) else measure)


if __name__ == "__main__":
    main()
