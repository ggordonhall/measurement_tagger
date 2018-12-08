# Measurement Tagger
[![Build Status](https://travis-ci.org/ggordonhall/measurement_tagger.png)](https://travis-ci.org/ggordonhall/measurement_tagger)
[![codecov](https://codecov.io/gh/ggordonhall/measurement_tagger/branch/master/graph/badge.svg)](https://codecov.io/gh/ggordonhall/measurement_tagger)

## A dependency parse based measurement tagger.

Text to be tagged should be stored in the `text/` directory. The file to tag is specific with `-t`.

Run in mode (`-m`):

| Mode    | Measurement   |
| --------|:-------------:|
| `d`     | Distance      |
| `t`     | Time          |
| `m`     | Mass          |
| `e`     | Energy        |
| `v`     | Volume        |

By default, tags measurements then convertes them to their standard unit. Unconverted measurements can be returned if run with the `--return_unconverted` flag. The maximum n-gram to search for measurement units, i.e. `nautical miles`, can be set with the 
`--max_gram` flag.

Run `pipenv install && python -m spacy download en` to setup, then test by running `main.py -m d -t wiki.txt`.

## TO DO

- [ ] Fix `--parallel` flag
- [x] Improve handling of n-gram measurement units
