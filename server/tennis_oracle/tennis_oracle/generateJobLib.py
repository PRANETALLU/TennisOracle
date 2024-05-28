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

logModel = LogisticRegression(penalty='l2', max_iter=100, random_state=42)

def bmi_index(weight, height):
    if height == 0:
        return 0
    else:
        return weight / (height ** 2)