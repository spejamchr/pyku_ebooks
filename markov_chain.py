import re
from syllable_counter import SyllableCounter

class MarkovChain:


    def __init__(self, ml):
        self.max_links = ml
        self.markov_chains = []
        self.files = []
        self.syllable_counter = SyllableCounter()
        self.updated = False

        self.__init_ml()


    def __init_ml(self):
        for i in range(len(self.markov_chains), self.max_links + 1):
            self.markov_chains.append({})

    def __getitem__(self, index):
        """Allows `markov_chain[1]`"""
        if index > self.max_links:
            raise IndexError(
                "index ({}) cannot be greater than max_links ({})"
                .format(index, self.max_links)
            )

        return self.markov_chains[index]

    def __setitem__(self, index, value):
        """Allows `markov_chain[1] = {}`"""
        if index > self.max_links:
            raise IndexError(
                "index ({}) cannot be greater than max_links ({})"
                .format(index, self.max_links)
            )

        self.markov_chains[index] = value
        return value

    def reset_max_links(self, ml):
        self.max_links = ml
        self.__init_ml()
        return ml

    def add_text(self, text):
        """Add some text to the markov chain"""
        self.updated = True
        spaces = re.compile(r"\s+")
        words = spaces.split(text)
        for i in range(self.max_links + 1):
            self.__add_to_markov_chains(i, words)

    def add_text_from_filename(self, filename):
        if filename in self.files: return

        with open(filename, "r") as f:
            self.add_text(f.read())
            self.files.append(filename)


    def chain_from_words(self, words):
        """Get an array of words that follow a phrase

        @param `words` is an array of words
        """
        chain = self[len(words)]
        if words in chain:
            return chain[words]
        else:
            return []

    def __add_to_markov_chains(self, n, words):
        for i in range(len(words) - n):
            group = words[i:i+n+1]
            word = group[-1]
            key = tuple(group[0:-1])
            if not key in self[n]:
                self[n][key] = []

            syllables = self.syllable_counter.syllables(word)
            if syllables == 0: continue

            self[n][key].append((word, syllables))


if __name__ == "__main__":
    mc = MarkovChain(2)
    mc.add_text("Hello there! How are you? I hope you are well there! Hello again!")
