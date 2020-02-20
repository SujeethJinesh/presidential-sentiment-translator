from party_affiliation import PartyAffiliation


class Candidate:
    def __init__(self, name: str, twitter_handle: str, party_affiliation: PartyAffiliation):
        self.name = name
        self.twitter_handle = twitter_handle
        self.party_affiliation = party_affiliation
