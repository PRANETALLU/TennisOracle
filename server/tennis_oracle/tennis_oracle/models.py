from django.db import models

class TennisPlayer(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.TextField()
    hand = models.IntegerField()
    height = models.IntegerField(null=True)
    country = models.TextField()
    age = models.IntegerField()
    total_w_aces = models.IntegerField(default=0)
    total_w_df = models.IntegerField(default=0)
    total_l_aces = models.IntegerField(default=0)
    total_l_df = models.IntegerField(default=0)
    rank = models.IntegerField()
    rank_points = models.IntegerField()
    num_of_wins = models.IntegerField(default=0)
    num_of_loss = models.IntegerField(default=0)
    no_of_matches = models.IntegerField(default=0)
    total_minutes = models.IntegerField(default=0)
    #matches = models.ManyToManyField('Match', through='MatchPlayer')
    class Meta:
        app_label = 'tennis_oracle'
    
class Match(models.Model):
    tournament = models.TextField()
    surface = models.TextField()
    score = models.TextField()
    minutes = models.IntegerField()
    winner = models.ForeignKey(TennisPlayer, related_name='won_matches', on_delete=models.CASCADE)
    loser = models.ForeignKey(TennisPlayer, related_name='lost_matches', on_delete=models.CASCADE)
    class Meta:
        app_label = 'tennis_oracle'
