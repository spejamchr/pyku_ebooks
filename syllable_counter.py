
import re

class SyllableCounter:
    """Count syllables in English strings

    Usage:

        > counter = SyllableCounter()
        > counter.syllables("How many syllable have I got? I've got lots.")
        12

    """

    # special cases: 1 syllable less than expected
    SUBTRACTIONS = [
        re.compile(r"[^AEIOU]E$"), # give, love, bone, done, ride ...
        re.compile(r"[AEIOU](?:([CFGHKLMNPRSVWZ])\1?|CK|SH|[RT]CH)E[DS]$"),
        # (passive) past participles and 3rd person sing present verbs:
        # bared, liked, called, tricked, bashed, matched

        re.compile(r".E(?:LY|LESS(?:LY)?|NESS?|FUL(?:LY)?|MENTS?)$"),
        # nominal, adjectival and adverbial derivatives from -e$ roots:
        # absolutely, nicely, likeness, basement, hopeless
        # hopeful, tastefully, wasteful

        re.compile(r"ION"), # action, diction, fiction
        re.compile(r"[CT]IA[NL]"), # special(ly), initial, physician, christian
        re.compile(r"[^CX]IOU"), # illustrious, NOT spacious, gracious, anxious, noxious
        re.compile(r"SIA$"), # amnesia, polynesia
        re.compile(r".GUE$"), # dialogue, intrigue, colleague
    ]

    # special cases: 1 syllable more than expected
    ADDITIONS = [
        re.compile(r"I[AIOU]"), # alias, science, phobia
        re.compile(r"[DLS]IEN"), # salient, gradient, transient
        re.compile(r"[AEIOUYM]BLE$"), # -Vble, plus -mble
        re.compile(r"[AEIOU]{3}"), # agreeable
        re.compile(r"^MC"), # mcwhatever
        re.compile(r"ISM$"), # sexism, racism
        re.compile(r"(?:([^AEIOUY])\1|CK|MP|NG)LE$"), # bubble, cattle, cackle, sample, angle
        re.compile(r"DNT$"), # couldnt
        re.compile(r"[AEIOU]Y[AEIOU]") # annoying, layer
    ]

    RAW_DICT = "data/cmudict-0.7b.txt"
    PARSED_DICT = "data/cmudict-parsed.txt"


    def __init__(self):
        try:
            with open(self.PARSED_DICT) as f:
                lines = f.readlines()
                self.words = {}
                for line in lines:
                    word, str_count = line.split(' ')
                    self.words[word] = int(str_count)

        except FileNotFoundError:
            self.__parse_dictionary()


    def __parse_dictionary(self):
        """Parse the CMU dictionary and save it to a file"""
        self.words = {}

        with open(self.RAW_DICT, "r") as f:
            lines = f.readlines()
            beginning_letter = re.compile(r"^[A-Z]")
            ending_number = re.compile(r"\(\d+\)$")
            anything_but_letters_and_apoststraphe = re.compile(r"[^A-Z']")
            non_letters = re.compile(r"[^A-Z]")
            syllable_indicators = re.compile(r"[012]")

            for line in lines:
                # if the line doesn't start with a letter, it's either a
                # comment or a special character I'm not interested in
                if not beginning_letter.match(line): continue

                word, syllables = line.split("  ")
                word = ending_number.sub("", word)
                if anything_but_letters_and_apoststraphe.search(word): continue

                word = non_letters.sub("", word)
                syllables = len(syllable_indicators.findall(syllables))

                if (not word in self.words) or syllables < self.words[word]:
                    self.words[word] = syllables

            with open(self.PARSED_DICT, "w") as p:
                for word, syllables in self.words.items():
                    p.write("{} {}\n".format(word, syllables))


    def syllables(self, string):
        apostrophe = re.compile(r"'")
        non_letters = re.compile(r"[^A-Z]")

        string = apostrophe.sub("", string.upper())
        words = non_letters.split(string)

        # `words` can be empty for strings without letters, like dates. Let's
        # disallow such words from appearing in the haiku.
        if len(words) == 0: return 18

        return sum([ self.__single_word_syllables(word) for word in words ])


    def __single_word_syllables(self, word):
        if len(word) == 0: return 0
        if word in self.words:
            return self.words[word]

        maybe = self.__guess(word)
        print("Word not in dictionary: \"{}\". Guessed {} syllables".format(word, maybe))
        self.words[word] = maybe
        return maybe


    def __guess(self, word):
        if len(word) == 1: return 1

        vowels = re.compile(r"[AEIOUY]+")

        syllables = len(vowels.findall(word))

        for pattern in self.SUBTRACTIONS:
            if pattern.search(word):
                syllables -= 1

        for pattern in self.ADDITIONS:
            if pattern.search(word):
                syllables += 1

        if syllables < 1:
            # No vowels?
            syllables = 1

        return syllables




if __name__ == "__main__":
    sc = SyllableCounter()

    c = sc.syllables("How many syllables have I got? I've got lots.")
    c = sc.syllables("How many syllables have I got? I've got lots.")
    c = sc.syllables("How many syllables have I got? I've got lots.")
    print(c)
