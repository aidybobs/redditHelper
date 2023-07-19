import os, string, praw, sys, json
from abc import ABC, abstractmethod
import PySimpleGUI as sg
from statistics import mode
from PyQt5 import QtWidgets, uic
from collections import Counter

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

class RedditHot(RedditSource):
    def __init__(self) -> None:
        self.reddit_con = super().connect()
        self.hot_submissions = []

    def fetch(self, limit: int, sub: string):
        self.hot_submissions = self.reddit_con.subreddit(sub).hot(limit=limit)

    def outTitles(self):
        titles = []
        for submission in self.hot_submissions:
            titles.append(vars(submission)["title"])
        return titles
    
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('resources/window.ui', self)
        self.button = self.findChild(QtWidgets.QPushButton, "Go")
        self.button.clicked.connect(self.findTop)
        self.textBrowser = self.findChild(QtWidgets.QTextBrowser, "textBrowser")
        self.sub = self.findChild(QtWidgets.QTextEdit, "textEdit")
        self.show()    
    
    def findTop(self):
        f = open('resources/words.json')
        data = json.load(f)
        popular_words = [i for i in data['commonWords']]
        reddit_top = RedditHot()
        reddit_top.fetch(limit=100, sub=self.sub.toPlainText())
        titles = reddit_top.outTitles()
        temp = [wrd for sub in titles for wrd in sub.split()]
        cleantemp = remove_punctuation(temp)
        newtemp = [word for word in cleantemp if word.lower() not in popular_words]
        top = most_popular(newtemp)
        self.textBrowser.setPlainText("\n".join(top))
        f.close()



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

def most_popular(input_list, n=11):
    word_counts = Counter(word.lower() for word in input_list)
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    most_popular_words = [word for word, count in sorted_words[:n] if word.strip()]
    return most_popular_words


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()