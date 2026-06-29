
from django.contrib import admin

from election.models import Election, States, Constituency, Candidate, Voters, Symbol

admin.site.register(Election)
admin.site.register(States)
admin.site.register(Constituency)
admin.site.register(Candidate)
admin.site.register(Voters)
admin.site.register(Symbol)
