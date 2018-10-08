
from reddit_reader import RedditReader
from markov_chain import MarkovChain
from writer import Writer

class PykuEbooks:
    """Generate Markov Chain haikus from Reddit source material"""

    def __init__(self, ml, subreddit, location):
        """Initialize the Markov Chain and writer

        ml:
            MarkovChain's max_links
        subreddit:
            The subreddit to use as the text source
        location:
            "posts"|"comments" - Whether to get the text from the top posts in
            the subreddit (faster), or from the children comments of the top
            posts in the subreddit (can return more text).
        sources:
            An array of strings for the MC
        """
        rr = RedditReader(subreddit)
        if location == "posts":
            texts = rr.get_many_post_bodies()
        elif location == "comments":
            texts = rr.get_many_comment_bodies()
        else:
            raise TypeError('`location` must be either "posts" or "comments"')

        self.mc = MarkovChain(ml)
        for text in texts:
            self.mc.add_text(text)

        self.w = Writer(self.mc)

    def haiku(self):
        return self.w.haiku()

if __name__ == "__main__":
    pe = PykuEbooks(4, "r/WritingPrompts", "comments")
    print(pe.haiku())
    print()
    print(pe.haiku())
    print()
    print(pe.haiku())
    print()
    print(pe.haiku())
    print()
    print()

    pe = PykuEbooks(4, "r/ocPoetry", "posts")
    print(pe.haiku())
    print()
    print(pe.haiku())
    print()
    print(pe.haiku())
    print()
    print(pe.haiku())
    print()
