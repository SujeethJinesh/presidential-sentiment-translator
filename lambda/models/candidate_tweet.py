from .candidate import Candidate


class CandidateTweet:
    def __init__(self, candidate: Candidate, text: str, tweet_id: int, sentiment=None):
        self.candidate = candidate
        self.text = text
        self.tweet_id = tweet_id
        self.sentiment = sentiment
