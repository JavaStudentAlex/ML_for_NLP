from argparse import ArgumentParser
from os.path import abspath

import nltk

from .log_likelihood import evaluate_trigrams

# init parser for CLI
parser = ArgumentParser(
    description="Evaluate trigrams importance with the likelihood ratio test")

# add arguments for CLI
parser.add_argument("-f", action="store", dest="file", type=str,
                    help="Get the path for the file with text")

# parse got arguments
args = parser.parse_args()

if args.directory:
    try:
        file_path = abspath(args.file)

        with open("static_idioms.txt", "rt") as file:
            line = "\n".join(file.readlines())

        with open("stopwords.txt", "rt") as file:
            stopwords = [stpwrd.strip().lower() for stpwrd in file.readlines()]

        tokens = nltk.RegexpTokenizer(r'\b[A-Za-z-]+\b').tokenize(line)

        tokens_with_no_stopwords = [token.lower() for token in tokens
                                    if token.lower() not in stopwords]

        first_20_trigrams = evaluate_trigrams(tokens_with_no_stopwords)
        result = "\n".join(first_20_trigrams)

    except FileNotFoundError:
        result = "Wrong file path! Please, try another one."
else:
    result = "No arguments in CLI"

print(result)