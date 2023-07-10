import os
import praw
from abc import ABC, abstractmethod

CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET_KEY = os.environ.get("SECRET_KEY")

class Source(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch(self):
        pass

class RedditSource(Source):
    def connect(self):
        self.reddit_con = praw.Reddit(client_id=CLIENT_ID,
                                      client_secret=SECRET_KEY,
                                      grant_type_access="client_credentials",
                                      user_agent="script/1,0")
        return self.reddit_con
    
    def fetch(self):
        pass

class RedditHotProgramming(RedditSource):
    def __init__(self) -> None:
        self.reddit_con = super().connect()
        self.hot_submissions = []

    def fetch(self, limit: int):
        self.hot_submissions = self.reddit_con.subreddit("programming").hot(limit=limit)

    def __repr__(self):
        titles = []
        for submission in self.hot_submissions:
            titles.append(vars(submission)["title"])
        return '\n'.join(titles)
    
if __name__ == "__main__":
    reddit_top_programming = RedditHotProgramming()
    reddit_top_programming.fetch(limit=10)
    print(reddit_top_programming)