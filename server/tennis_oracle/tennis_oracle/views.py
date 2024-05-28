from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import TennisPlayer, Match
from django.db.models import Q
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

table_name = TennisPlayer._meta.db_table
print("Table Name:", table_name)


logModel = LogisticRegression(penalty='l2', max_iter=100, random_state=42)

def bmi_index(weight, height):
    if height == 0:
        return 0
    else:
        return weight / (height ** 2)
    
def importPlayerData():
    dfs = []

    for year in range(2021, 2024):
        filename = f"tennis_oracle/ATP/atp_matches_{year}.csv"
        df = pd.read_csv(filename)
        dfs.append(df)
        
    merged_df = pd.concat(dfs, ignore_index=True)
    
    for index, row in merged_df.iterrows():
        winner_id = row['winner_id']
        loser_id = row['loser_id']
        
        total_w_aces = row['w_ace'] if not pd.isnull(row['w_ace']) else 0
        total_w_df = row['w_df'] if not pd.isnull(row['w_df']) else 0
        total_l_aces = row['l_ace'] if not pd.isnull(row['l_ace']) else 0
        total_l_df = row['l_df'] if not pd.isnull(row['l_df']) else 0
        row_Minutes = row['minutes'] if not pd.isnull(row['minutes']) else 0
        
        winner_id = row['winner_id']
        winner_name = row['winner_name']
        winner_hand = 1 if row['winner_hand'] == 'R' else 0
        winner_ht = row['winner_ht']
        winner_ioc = row['winner_ioc']
        winner_age = row['winner_age']
        winner_rank = row['winner_rank']
        winner_rank_points = row['winner_rank_points']
        
        
        if pd.isnull(row['winner_ht']) or pd.isnull(row['loser_ht']) or pd.isnull(row['winner_rank']) or pd.isnull(row['loser_rank']):
            continue

        existing_player = TennisPlayer.objects.filter(player_id=winner_id).first()
        

        if existing_player:
            existing_player.name = winner_name
            existing_player.hand = winner_hand
            existing_player.height = winner_ht
            existing_player.country = winner_ioc
            existing_player.age = winner_age
            existing_player.total_w_aces += total_w_aces
            existing_player.total_w_df += total_w_df
            existing_player.rank = winner_rank
            existing_player.rank_points = winner_rank_points
            existing_player.num_of_wins += 1
            existing_player.no_of_matches += 1
            existing_player.total_minutes += row_Minutes
            existing_player.save()
        else:
            existing_player = TennisPlayer.objects.create(
                player_id=winner_id,
                name=winner_name,
                hand=winner_hand,
                height=winner_ht,
                country=winner_ioc,
                age=winner_age,
                total_w_aces=total_w_aces,
                total_w_df=total_w_df,
                rank=winner_rank,
                rank_points=winner_rank_points,
                num_of_wins=1,
                num_of_loss=0,
                no_of_matches=1,
                total_minutes=row_Minutes
            )
            
        loser_name = row['loser_name']
        loser_hand = 1 if row['loser_hand'] == 'R' else 0
        loser_ht = row['loser_ht']
        loser_ioc = row['loser_ioc']
        loser_age = row['loser_age']
        loser_rank = row['loser_rank']
        loser_rank_points = row['loser_rank_points']

        existing_loser = TennisPlayer.objects.filter(player_id=loser_id).first()

        if existing_loser:
            existing_loser.name = loser_name
            existing_loser.hand = loser_hand
            existing_loser.height = loser_ht
            existing_loser.country = loser_ioc
            existing_loser.age = loser_age
            existing_loser.total_l_aces += total_l_aces
            existing_loser.total_l_df += total_l_df
            existing_loser.rank = loser_rank
            existing_loser.rank_points = loser_rank_points
            existing_loser.num_of_loss += 1
            existing_loser.no_of_matches += 1
            existing_loser.total_minutes += row_Minutes
            existing_loser.save()
        else:
            existing_loser = TennisPlayer.objects.create(
                player_id=loser_id,
                name=loser_name,
                hand=loser_hand,
                height=loser_ht,
                country=loser_ioc,
                age=loser_age,
                total_l_aces=total_l_aces,
                total_l_df=total_l_df,
                rank=loser_rank,
                rank_points=loser_rank_points,
                num_of_wins=0,
                num_of_loss=1,
                no_of_matches=1,
                total_minutes=row_Minutes
            )
            
        Match.objects.create(
            tournament=row['tourney_name'],
            surface=row['surface'],
            score=row['score'],
            minutes=row['minutes'] if not pd.isnull(row['minutes']) else 0,
            winner=existing_player,
            loser=existing_loser
        )
        
    return HttpResponse(TennisPlayer.objects.count())

def importPlayerTest1():
    playerList = TennisPlayer.objects.all()

    X = []
    Y = []
    
    for player in playerList:
        playerMatches = Match.objects.filter(Q(winner__name=player.name) | Q(loser__name=player.name))
        for playerMatch in playerMatches:
            
            x_components = []
        
            # Player 1
            player1 = player
            x_components.append(player1.hand)
            x_components.append(bmi_index(player1.age, player1.height / 100))
            x_components.append(player1.total_w_aces + player1.total_l_aces)
            x_components.append(player1.rank)
            x_components.append(player1.rank_points)
            x_components.append(player1.num_of_wins / (player1.num_of_wins + player1.num_of_loss) * 100)
            x_components.append(player1.no_of_matches)
            x_components.append(player1.total_minutes)
            
            player2Object = None
            if player1.player_id == playerMatch.winner.player_id:
                player2Object = playerMatch.loser
                Y.append(1)
            else:
                player2Object = playerMatch.winner
                Y.append(2)
        
            # Player2
            player2 = player2Object
            x_components.append(player2.hand)
            x_components.append(bmi_index(player2.age, player2.height / 100))
            x_components.append(player2.total_w_aces + player2.total_l_aces)
            x_components.append(player2.rank)
            x_components.append(player2.rank_points)
            x_components.append(player2.num_of_wins / (player2.num_of_wins + player2.num_of_loss) * 100)
            x_components.append(player2.no_of_matches)
            x_components.append(player2.total_minutes)
        
            X.append(x_components)
            
    X = np.array(X)
    Y = np.array(Y)
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, shuffle=True)
    
    logModel.fit(X_train, Y_train)
    
    Y_pred = logModel.predict(X_test)
    
    accuracyScore = accuracy_score(Y_test, Y_pred)

    return HttpResponse(accuracyScore * 100)

@csrf_exempt
def predict_Winner(request):
    
    if request.method == 'POST':
        #importPlayerData()
        if not TennisPlayer.objects.exists() and not Match.objects.exists():
            importPlayerData()
            
        body_unicode = request.body.decode('utf-8')
        body_params = json.loads(body_unicode)
            
        p1_name = body_params.get('p1_name')
        p2_name = body_params.get('p2_name')
        
        print("p1_name", p1_name)
        print("p2_name", p2_name)
        
        p1_object = TennisPlayer.objects.filter(name__iexact=p1_name).first()
        p2_object = TennisPlayer.objects.filter(name__iexact=p2_name).first()
        
        X_Features = []
        X_Features.append(p1_object.hand)
        X_Features.append(bmi_index(p1_object.age, p1_object.height / 100))
        X_Features.append(p1_object.total_w_aces + p1_object.total_l_aces)
        X_Features.append(p1_object.rank)
        X_Features.append(p1_object.rank_points)
        X_Features.append(p1_object.num_of_wins / (p1_object.num_of_wins + p1_object.num_of_loss) * 100)
        X_Features.append(p1_object.no_of_matches)
        X_Features.append(p1_object.total_minutes)
        
        X_Features.append(p2_object.hand)
        X_Features.append(bmi_index(p2_object.age, p2_object.height / 100))
        X_Features.append(p2_object.total_w_aces + p2_object.total_l_aces)
        X_Features.append(p2_object.rank)
        X_Features.append(p2_object.rank_points)
        X_Features.append(p2_object.num_of_wins / (p2_object.num_of_wins + p2_object.num_of_loss) * 100)
        X_Features.append(p2_object.no_of_matches)
        X_Features.append(p2_object.total_minutes)
        
        X_F = np.array(X_Features).reshape(1, -1)
        
        importPlayerTest1()
        
        Y_F = int(logModel.predict(X_F)[0])
        
        return JsonResponse({"Winner": Y_F})
    
    else:
        return JsonResponse("Only POST Requests are allowed")
  
@csrf_exempt  
def search_Filter(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_params = json.loads(body_unicode)
        
        hand1 = body_params.get('hand')
        country1 = body_params.get('country')
        minAge1 = body_params.get("minAge")
        maxAge1 = body_params.get("maxAge")
        name1 = body_params.get("name")
        rankRange = body_params.get("rankRange")
        minHeight = body_params.get("minHeight")
        maxHeight = body_params.get("maxHeight")
        
        players = TennisPlayer.objects.all()
        
        if hand1 and hand1 != "Select Hand":
            players = players.filter(hand=hand1)
        if country1 and country1 != "Select Country":
            players = players.filter(country=country1)
        if minAge1:
            players = players.filter(age__gte=int(minAge1))
        if maxAge1:
            players = players.filter(age__lte=int(maxAge1))
        if minHeight:
            players = players.filter(height__gte=int(minHeight))
        if maxHeight:
            players = players.filter(height__lte=int(maxHeight))
        if name1 and name1 != "Select Player Name":
            players = players.filter(name=name1)
        if rankRange and rankRange != "Select Rank":
            if rankRange == "0 - 100":
                players = players.filter(rank__range=(0, 100))
            if rankRange == "101 - 500":
                players = players.filter(rank__range=(101, 500))
            if rankRange == "501 - 1000":
                players = players.filter(rank__range=(501, 1000))
        
        return JsonResponse({"players": list(players.values())})
    else:
        return JsonResponse("Only POST Requests are allowed")
    
def getTennisPlayers(request):
    
    if request.method == 'GET':
        playerList = TennisPlayer.objects.order_by('name')
        return JsonResponse({"players": list(playerList.values())})
    else:
        return JsonResponse("Only GET Requests are allowed")
        