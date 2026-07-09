from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render

from election.models import States, Constituency, Election, Candidate, Voters, Vote
from election.utils import Voter, CastVote


def dashboard(request):
    return render(
        request,
        "dashboard.html",
        {
            "constituency": Constituency.objects.all(),
        }
    )

def state_details(request, state_id):
    return render(
        request,
        "details.html",
        context = {
            "state": States.objects.get(id=state_id)
        }
    )

def confirm_identity(request, election_id):
    return render(
        request,
        "confirm_identity.html",
        {
            "election": Election.objects.get(id=election_id),
            "error": request.GET.get("error"),
        }
    )

def validate_identity(request, election_id):
    # if validation successful
    print(request.GET)
    voter = Voter(request.GET.get("aadhaar")).get_voter()
    if not voter:
        error = "Identity not found"
        return HttpResponseRedirect(f"/confirm-identity/{election_id}?error={error}")

    return render(
        request,
        "cast_vote.html"
        ,{
            "election": Election.objects.get(id=election_id),
            "candidates": Candidate.objects.filter(election=election_id),
            "aadhaar": request.GET.get("aadhaar"),
        }
    )


def cast_vote(request):
    voter = Voters.objects.get(aadhaar=request.POST.get("aadhaar"))
    election_id = request.POST.get("election_id")
    cast_vote = CastVote(
        election_id, voter.id, request.POST.get("candidate_id")
    )
    result = cast_vote.save_vote()
    if result:
        message = "Casted vote successfully"
    else:
        message = "Casted vote failed"
    return render(
        request,
        "cast_vote.html",
        context={
            "message": message,
            "result": True,
            "election_results": Vote.objects.filter(election=election_id).aggregate(
                Sum("votes")
            ),
        }
    )


