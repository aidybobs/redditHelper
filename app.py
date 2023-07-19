import os
import praw
from abc import ABC, abstractmethod
import PySimpleGUI as sg
from statistics import mode
import string

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

    def outTitles(self):
        titles = []
        for submission in self.hot_submissions:
            titles.append(vars(submission)["title"])
        return titles
    
popular_words = [
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
    'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
    'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
    'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', '-',
    'for'
]

punctuation = [
    '.', ',', ';', ':', '!', '?', '"', "'", '(', ')', '[', ']', '{', '}', '<', '>',
    '/', '\\', '|', '@', '#', '$', '%', '^', '&', '*', '-', '_', '+', '=', '~'
]

def remove_punctuation(strings):
    # Define a translation table mapping punctuation marks to None
    translation_table = str.maketrans('', '', string.punctuation)

    # Remove punctuation from each string in the list
    cleaned_strings = [string.translate(translation_table) for string in strings]

    return cleaned_strings

if __name__ == "__main__":
    reddit_top = RedditHotProgramming()
    reddit_top.fetch(limit=10)
    titles = reddit_top.outTitles()
    temp = [wrd for sub in titles for wrd in sub.split()]
    cleantemp = remove_punctuation(temp)
    newtemp = [word for word in cleantemp if word.lower() not in popular_words]
    top = []
    i = 0
    while i<=9:
        if mode(newtemp) != '':
            top.append(mode(newtemp))
            newtemp.remove(mode(newtemp))
            i += 1
        else:
            newtemp.remove(mode(newtemp))
    print("\n".join(top))