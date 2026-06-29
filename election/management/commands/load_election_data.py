from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from election.models import Candidate, Constituency, Election, Symbol, Vote, Voters


SYMBOL_NAMES = [
    "Lotus",
    "Hand",
    "Broom",
    "Bicycle",
    "Lantern",
    "Star",
]

VOTER_FIRST_NAMES = [
    "Aarav",
    "Aditi",
    "Arjun",
    "Diya",
    "Ishaan",
    "Kavya",
    "Meera",
    "Neha",
    "Rohan",
    "Vivaan",
]

VOTER_LAST_NAMES = [
    "Sharma",
    "Verma",
    "Thakur",
    "Kapoor",
    "Mehta",
    "Rana",
    "Chauhan",
    "Sood",
    "Gupta",
    "Joshi",
]

CANDIDATE_FIRST_NAMES = [
    "Ananya",
    "Bhavesh",
    "Charu",
    "Dev",
    "Esha",
    "Farhan",
]

CANDIDATE_LAST_NAMES = [
    "Sharma",
    "Verma",
    "Rana",
    "Chauhan",
    "Kapoor",
    "Sood",
]


def get_or_create_first(model, defaults=None, **lookup):
    instance = model.objects.filter(**lookup).first()
    if instance:
        return instance, False
    params = {**lookup, **(defaults or {})}
    return model.objects.create(**params), True


class Command(BaseCommand):
    help = "Load sample voters, candidates, and symbols without creating Vote records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--voters-per-constituency",
            type=int,
            default=10,
            help="Number of voters to create for each constituency. Defaults to 10.",
        )
        parser.add_argument(
            "--candidates-per-constituency",
            type=int,
            default=3,
            help="Number of candidates to create for each constituency. Defaults to 3.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        voters_per_constituency = options["voters_per_constituency"]
        candidates_per_constituency = options["candidates_per_constituency"]

        if voters_per_constituency < 1:
            raise CommandError("--voters-per-constituency must be at least 1.")
        if candidates_per_constituency < 1:
            raise CommandError("--candidates-per-constituency must be at least 1.")

        constituencies = list(Constituency.objects.order_by("id"))
        if not constituencies:
            raise CommandError("No constituencies found. Create constituencies before loading election data.")

        vote_count_before = Vote.objects.count()
        created_symbols = created_voters = created_candidates = updated_candidates = 0

        symbols = []
        for symbol_name in SYMBOL_NAMES:
            symbol, created = get_or_create_first(Symbol, name=symbol_name)
            symbols.append(symbol)
            created_symbols += int(created)

        for constituency in constituencies:
            election = (
                Election.objects.filter(constituency=constituency)
                .order_by("-start_session", "-id")
                .first()
            )

            for index in range(voters_per_constituency):
                first_name = VOTER_FIRST_NAMES[index % len(VOTER_FIRST_NAMES)]
                last_name = VOTER_LAST_NAMES[(constituency.id + index) % len(VOTER_LAST_NAMES)]
                voter_name = f"{first_name} {last_name} {constituency.name}"
                _, created = get_or_create_first(
                    Voters,
                    name=voter_name,
                    constituency=constituency,
                )
                created_voters += int(created)

            for index in range(candidates_per_constituency):
                first_name = CANDIDATE_FIRST_NAMES[index % len(CANDIDATE_FIRST_NAMES)]
                last_name = CANDIDATE_LAST_NAMES[(constituency.id + index) % len(CANDIDATE_LAST_NAMES)]
                symbol = symbols[index % len(symbols)]
                candidate_name = f"{first_name} {last_name} {constituency.name}"
                candidate, created = get_or_create_first(
                    Candidate,
                    name=candidate_name,
                    constituency=constituency,
                    symbol=symbol,
                )
                created_candidates += int(created)

                if election and candidate.election_id != election.id:
                    candidate.election = election
                    candidate.save(update_fields=["election"])
                    updated_candidates += 1

        vote_count_after = Vote.objects.count()
        if vote_count_after != vote_count_before:
            raise CommandError("Vote table changed unexpectedly; rolling back.")

        self.stdout.write(
            self.style.SUCCESS(
                "Loaded election data: "
                f"{created_symbols} symbols, "
                f"{created_voters} voters, "
                f"{created_candidates} candidates created; "
                f"{updated_candidates} candidates updated; "
                f"{vote_count_after} votes present."
            )
        )
