# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

class NewsStory(object):
    """RSS feed class that stores guid, title, subject, summary and link for each feed"""
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link
#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__(self, word):
        super(WordTrigger, self).__init__()
        self.word = word.lower()

    @staticmethod
    def get_text_words(text):
        """Recives a text, split the text as it consider punctuation and space as seperators.
            Return A list of words after splitting"""
        intab = string.punctuation
        outtab = " " * len(intab)
        transtab = string.maketrans(intab, outtab)
        return text.lower().translate(transtab).split(' ')

    def is_word_in(self, text):
        return self.word in self.get_text_words(text)
        

class TitleTrigger(WordTrigger):
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_word_in(story.get_title())
        
class SubjectTrigger(WordTrigger):
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_word_in(story.get_subject())

class SummaryTrigger(WordTrigger):
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.is_word_in(story.get_summary())


# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        super(NotTrigger, self).__init__()
        self.trigger = trigger

    def evaluate(self, story):
        """Fire on a news story by inverting the output of the inputted trigger"""
        return not self.trigger.evaluate(story)

# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        super(AndTrigger, self).__init__()
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger

    def evaluate(self, story):
        """Fire on a news story only if both of the inputted triggers would fire on that item"""
        return self.first_trigger.evaluate(story) and self.second_trigger.evaluate(story)
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        super(OrTrigger, self).__init__()
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger

    def evaluate(self, story):
        """Fire on a news story only if either one of the inputted triggers would fire on that item"""
        return self.first_trigger.evaluate(story) or self.second_trigger.evaluate(story)

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        super(PhraseTrigger, self).__init__()
        self.phrase = phrase
    
    def evaluate(self, story):
        """Fire when a given phrase is in any of the subject, title, or summary"""
        return self.phrase in story.get_subject() or \
            self.phrase in story.get_title() or \
            self.phrase in story.get_summary()

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break 
    return filtered_stories

#======================
# Part 4
# User-Specified Triggers
#======================


def create_basic_trigger(t_type, arg):
    if t_type == 'SUBJECT':
        return SubjectTrigger(arg[0])
    elif t_type == 'TITLE':
        return TitleTrigger(arg[0])
    elif t_type == 'SUMMARY':
        return SummaryTrigger(arg[0])
    elif t_type == 'PHRASE':
        return PhraseTrigger(' '.join(arg))

def create_composite_trigger(t_type, args, triggers):
    if t_type == 'NOT':
        operand_trigger = triggers[args[0]]
        return NotTrigger(operand_trigger)
    first_trigger = triggers[args[0]]
    second_trigger = triggers[args[1]]
    if t_type == 'AND':
        return AndTrigger(first_trigger, second_trigger)
    elif t_type == 'OR':
        return OrTrigger(first_trigger, second_trigger)


def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    basic_triggers = ['SUBJECT', 'TITLE', 'SUMMARY', 'PHRASE']
    composite_triggers = ['NOT', 'AND', 'OR']
    triggers = []
    # To save triggers by string keys corresponds to the name written into config
    triggers_tmp = {}
    # Parse lines
    for line in lines:
        words = line.split(' ')
        if words[0] == 'ADD':
            for trig_name in words[1:]:
                triggers.append(triggers_tmp[trig_name])
        elif words[1] in basic_triggers:
            triggers_tmp[words[0]] = create_basic_trigger(words[1], words[2:])
        elif words[1] in composite_triggers:
            triggers_tmp[words[0]] = create_composite_trigger(words[1], words[2:], triggers_tmp)
    return triggers
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

