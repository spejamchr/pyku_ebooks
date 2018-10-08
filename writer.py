
import re
import random
from markov_chain import MarkovChain

class Writer:

    LAST_QUERY = re.compile("[\\.\\?\\!]['\"]?$")
    FIRST_QUERY = re.compile(r"^[^a-z]*[A-Z]")

    def __init__(self, markov_chain):
        self.markov_chain = markov_chain

    def haiku(self):
        """Generate a random haiku"""
        ml = self.markov_chain.max_links
        line1 = self.__line(syllables=5, before=(), first=True)
        before = tuple(line1[-ml:])
        line2 = self.__line(syllables=7, before=before)
        before = tuple((line1 + line2)[-ml:])
        line3 = self.__line(syllables=5, before=before, last=True)
        return "\n".join([" ".join(l) for l in [line1, line2, line3]])

    def syllables(self, word):
        return self.markov_chain.syllable_counter.syllables(word)

    def __line(self, *, syllables, before, first=False, last=False):
        """Return an array of words as specified

        syllables: How many syllables (total) the words must have
        before: The seed word(s) that came before, passed as an tuple of words
        first: True/False. If true, the first word will be capitalized
        last: True/False. If true, the last word will end in one of [.?!]
        """
        ml = self.markov_chain.max_links

        first_word_t = self.__random_word(syllables, before, first, last)
        words = [first_word_t[0]]
        current_syllables = first_word_t[1]
        before = (before + (first_word_t[0],))[-ml:]

        while current_syllables < syllables:
            maximum = syllables - current_syllables
            new_word_t = self.__random_word(maximum, before, False, last)
            current_syllables += new_word_t[1]

            words.append(new_word_t[0])

            before = (before + (new_word_t[0],))[-ml:]

        return words

    def __random_word(self, maximum, before, first, last):
        """Return a random word from the markov chain

        maximum: The maximum syllables the world may have
        before: The seed word(s) that came before, passed as an tuple of words
        first: True/False. If true, the word will be capitalized
        last: True/False. If true, the word will end in one of [.?!] if it has
            the maximum number of syllables
        """
        words = self.__possible_next_words(maximum, before, first, last)

        if len(words) == 0:
            msg = """No available words!
            maximum={}
            before={}
            first={}
            last={}
            """.format(maximum, before, first, last)
            raise IndexError(msg)

        return words[random.randrange(len(words))]


    def __possible_next_words(self, maximum, before, first, last):
        """Return possible next words from the markov chain"""
        filterer = self.__filterer(maximum, before, first, last)
        word_tuples = self.markov_chain.chain_from_words(before)
        return [wt for wt in word_tuples if filterer(wt)]

    def __filterer(self, maximum, before, first, last):
        """Create a word filterer that can be used for many words"""
        def filt(wt):
            """Determine if this word tuple is appropriate or not"""
            w, s = wt
            if s > maximum:
                return False
            if first and (not self.FIRST_QUERY.match(w)):
                return False
            if last and s == maximum and (not self.LAST_QUERY.search(w)):
                return False
            return True

        return filt





if __name__ == "__main__":
    mc = MarkovChain(2)
    mc.add_text("This is a haiku. Written today (of all days). And it's not finished. This is a haiku. Written today (of all days). And it's not finished.")
    w = Writer(mc)
    print(w.haiku())
