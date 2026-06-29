from django.http import HttpResponseRedirect
from django.shortcuts import render

from election.models import States, Constituency, Election, Candidate
from election.utils import Voter


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
            "candidates": Candidate.objects.filter(election=election_id)
        }
    )


