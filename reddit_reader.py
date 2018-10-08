
import json
import multiprocessing

from urllib.request import Request, urlopen


class RedditReader:
    """Grab some hot text from some reddit"""

    BASE_URL = "https://www.reddit.com/"


    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.__sub_json = None


    def base_url(self):
        """The base subreddit url, without a format extension"""
        return "{}{}".format(self.BASE_URL, self.subreddit)


    def subreddit_url(self):
        return "{}.json".format(self.base_url())

    def sub_json(self):
        if not self.__sub_json:
            self.__sub_json = self.get_json(self.subreddit_url())

        return self.__sub_json


    def posts(self):
        """Get the currently hottest posts in the subreddit"""
        not_stickied = lambda c: not c['data']['stickied']
        children = self.sub_json()['data']['children']
        return [c['data'] for c in children if not_stickied(c)]


    def listing_url(self, listing_id):
        """Get the json endpoint for a listing given its id"""
        return "{}/comments/{}.json".format(self.base_url(), listing_id)


    def get_json(self, url):
        """Get and parse the json from some url"""
        req = Request(url)
        req.add_header("User-agent", "pyku_ebooks 0.1")
        return json.loads(urlopen(req).read())


    def children_bodies(self, listing_id):
        """Get the text of all immediate children of some listing"""
        j = self.get_json(self.listing_url(listing_id))
        children = j[1]['data']['children']

        def condition(child):
            """Only return posts that fit these criterion"""
            if not 'data' in child: return False
            if not 'body' in child['data']: return False
            return not child['data']['stickied']

        return [c['data']['body'] for c in children if condition(c)]

    def get_many_comment_bodies(self):
        """Get the text of many comments of the top posts of the subreddit"""
        pool = multiprocessing.Pool()
        post_ids = [p['id'] for p in self.posts()]
        body_groups = pool.map(self.children_bodies, post_ids)
        return [body for group in body_groups for body in group]

    def get_many_post_bodies(self):
        """Get the text of the top posts of the subreddit"""
        return [p['selftext'] for p in self.posts()]


if __name__ == "__main__":
    r = RedditReader("r/ocPoetry")
    print(r.get_many_post_bodies())
