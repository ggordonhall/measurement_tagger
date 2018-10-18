# Measurement Tagger
## A dependency parse based measurement tagger.

Text to be tagged should be stored in the `text/` directory. The file to tag is specific with `-t`.

Run in mode (`-m`):
    `d`: Distance
    `t`: Time
    `m`: Mass
    `e`: Energy
    `v`: Volume

By default, tags measurements then convertes them to their standard unit. Unconverted measurements can be returned if run with the `--return_unconverted` flag.

Run `pipenv install && python -m spacy download en` to setup, then test by running `main.py -m d -t wiki.txt`.
