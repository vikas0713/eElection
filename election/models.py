from django.db import models


class States(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.name


class Constituency(models.Model):

    name = models.CharField(max_length=100)
    population = models.IntegerField()
    description = models.TextField(blank=True, null=True, default='')
    state = models.ForeignKey(States, on_delete=models.SET_NULL, blank=True, null=True, related_name='constituencies')

    def __str__(self):
        return self.name


class Election(models.Model):

    start_session = models.DateTimeField()
    end_session = models.DateTimeField()
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.start_session.strftime("%B %d, %Y")


class Symbol(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Voters(models.Model):
    name = models.CharField(max_length=100)
    aadhaar = models.CharField(max_length=100, db_index=True)
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=models.SET_NULL, blank=True, null=True)
    symbol = models.ForeignKey(Symbol, on_delete=models.SET_NULL, blank=True, null=True)
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.name} -- {self.constituency.name}'

class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.SET_NULL, blank=True, null=True)
    casted_by = models.ForeignKey(Voters, on_delete=models.SET_NULL, blank=True, null=True)
    casted_to = models.ForeignKey(Candidate, on_delete=models.SET_NULL, blank=True, null=True)
    casted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Vote {self.pk}"


