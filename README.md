# pyku_ebooks

Tweet random haikus

[See the result on Twitter](https://twitter.com/EbooksHaiku)

I like Markov Chains, and I like haikus, so this is my attempt at creating a
Twitter bot that tweets Markov-Chain-generated haikus. It's not meant to be
blazing fast, but it should count syllables fairly accurately. Oh, and it uses
Reddit for source texts, so yay!

## Examples

Tweet a random haiku:

```bash
python3 /path/to/pyku_ebooks/tweet.py
```

The first time will take longer than normal (~1 minute), because it has to
parse the CMU pronunciation dictionary for word syllable lengths. Subsequent
runs should run more quickly.

Every time you run `tweet.py` the program grabs some text using the [reddit
API](https://www.reddit.com/dev/api/) from the front page of either
`/r/WritingPrompts` or `/r/ocPoetry` (randomly) and builds a Markov Chain from
it. Because it fetches and compiles the chains every time, it can be a little
slow.

If you'd rather use static source texts and persistant Markov Chains, take a
look at [spejamchr/haiku_ebooks](https://github.com/spejamchr/haiku_ebooks).
This repo is a port of that one, designed to run from a Raspberry Pi that
already has Python installed.

## Requirements

- `python3` (I'm using `python 3.7.0`)
- [`twitter`](https://pypi.org/project/twitter/) for tweeting

## Install

> Heads up: this is more a collection of scripts than a package.

- Clone the git repo: `git clone https://github.com/spejamchr/pyku_ebooks.git`
- Make sure `twitter` is installed too: `pip install twitter`
- Rename `keys.example.yml` to `keys.yml` and put your Twitter keys
  and access tokens in there

## Author

Original author: Spencer Christiansen

## License

haiku_ebooks is released under the [MIT License](https://opensource.org/licenses/MIT).
