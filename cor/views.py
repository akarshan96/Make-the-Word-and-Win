from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import WordOfTheDay, AllFields, Pool
from django.db.models import Sum
from django.http import HttpResponse
from django.http import JsonResponse
import random
import operator

@login_required
def home(request):

    obj, created = AllFields.objects.get_or_create(
        user = request.user,
        defaults={ 
            'earning' : 0,
            'pulls' : 0,
            'lettersfound' : ""
        }
    )

    word = WordOfTheDay.objects.all()
    wordoftheday = str(word[0])
    fields = AllFields.objects.all().filter(user = request.user)
    
    #sumofpulls = AllFields.objects.aggregate(Sum('pulls')).values()
    #sumofearnings = AllFields.objects.aggregate(Sum('earning')).values()
    moneypool = Pool.objects.all() 
    prize = int(20/100 * int(moneypool[0].moneypooled))
    top = AllFields.objects.order_by('-earning')[:10]

    args = {'WordOfTheDay': wordoftheday, 'Fields':fields[0], 'Prize':prize, 'Top':top}
    


    return render(request, 'home.html', args) 

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def generaterandom(request):

    enable = True
    pool_a = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']

    word = WordOfTheDay.objects.all()
    wordoftheday = str(word[0])

    pool_b = list(wordoftheday)
    fields = AllFields.objects.get(user = request.user)
    fields.pulls = int(fields.pulls) + 1
    fields.save()

    pool = Pool.objects.all()[0]
    pool.moneypooled = int(pool.moneypooled) + 1
    pool.save()


    pool_b = list(set(pool_b) - set((list(fields.lettersfound))))

    p = decide_probabity(word, fields)
    letter = None
    if pool_b != []:
        for x in pool_b:
            if x in pool_a:
                pool_a.remove(x)
        if random.random() < p:   
            x = random.randint(0, len(pool_b) - 1)
            letter = pool_b[x]
        else:
            x = random.randint(0, len(pool_a) - 1)
            letter = pool_a[x]
        print (letter)

        if letter in wordoftheday:
            if letter not in fields.lettersfound:
                fields.lettersfound = str(fields.lettersfound) + letter
                fields.save()
            
    else:
        letter = "won"
        fields.earning = int(fields.earning + 20/100 * pool.moneypooled)
        pool.moneypooled = int(pool.moneypooled - 20/100 * pool.moneypooled)
        pool.save()
        fields.save()
        enable = False

    jsonstring = {'status': letter, 'enable': enable}
    return JsonResponse(jsonstring)


def decide_probabity(wordoftheday, allfeilds):
    word = wordoftheday
    sum_of_pulls = list(AllFields.objects.aggregate(Sum('pulls')).values())[0]
    print(sum_of_pulls)

    pool = Pool.objects.all()[0]
    money = int(pool.moneypooled)

    fields = allfeilds
    no_of_letters_found = len(str(fields.lettersfound))

    #setting probabilties for different scenarios
    if (sum_of_pulls < 20000 or money < 20000):
        return 0
    else:
        if no_of_letters_found == len(word) - 1:
            return 0.05
        elif no_of_letters_found == len(word) - 2:
            return 0.10
        elif no_of_letters_found == len(word) - 3:
            return 0.15
        else:
            return 0.20
