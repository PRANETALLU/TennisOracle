from django.contrib import admin

from tennis_oracle.models import TennisPlayer

from tennis_oracle.models import Match

admin.site.register(TennisPlayer)

admin.site.register(Match)