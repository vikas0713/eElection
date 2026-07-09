import datetime

from election.models import Election, Candidate, Voters, Constituency, Vote


class CastVote:

    def __init__(self, election_id, voter_id, candidate_id):
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        self.election_id = election_id

    def get_election(self):
        return Election.objects.get(id=self.election_id)

    def get_candidate(self):
        return Candidate.objects.get(id=self.candidate_id,election_id=self.election_id)

    def get_voter(self):
        return Voters.objects.get(id=self.voter_id)

    def get_constituency(self):
        return self.get_candidate().constituency

    def validate_election(self):
        election = self.get_election()
        time_now = datetime.datetime.now(tz=datetime.timezone.utc)
        if time_now.date() == election.start_session.date():
            return True
        return False

    def match_candidate_constituency(self):
        candidate = self.get_candidate()
        voter = self.get_voter()
        if candidate.constituency_id != voter.constituency_id:
            return False
        return True

    def is_already_voted(self):
        if Vote.objects.filter(
                election_id=self.election_id,
                casted_to_id=self.candidate_id,
                casted_by_id=self.voter_id
        ).exists():
            return True
        return False


    def save_vote(self):
        # validating election
        if not self.validate_election():
            return False
        # validate constituency of candidate and voter
        if not self.match_candidate_constituency():
            return False
        # save vote at last
        if self.is_already_voted():
            return False
        time_now = datetime.datetime.now(tz=datetime.timezone.utc)
        vote_obj = Vote(
            election_id=self.election_id,
            casted_by_id=self.voter_id,
            casted_to_id=self.candidate_id,
            casted_at=time_now,
        )
        vote_obj.save()
        return True



class Voter:

    def __init__(self, a_id):
        self.a_id = a_id

    def get_voter(self):
        try:
            voter = Voters.objects.get(aadhaar=self.a_id)
            return voter
        except Voters.DoesNotExist:
            return False






