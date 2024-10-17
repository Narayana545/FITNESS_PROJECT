from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm
from django.db.models import Sum
from .models import Goal, Achievement,Leaderboard
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request,'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

def set_goal(request):
    if request.method == 'POST':
        goal_name = request.POST['goal_name']
        target_value = request.POST['target_value']
        goal = Goal.objects.create(user=request.user, goal_name=goal_name, target_value=target_value)
        return redirect('dashboard')
    return render(request, 'set_goal.html')

def achieve_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    if request.method == 'POST':
        value = int(request.POST['value'])
        goal.current_value += value
        if goal.current_value >= goal.target_value:
            goal.achieved = True
        goal.save()
        Achievement.objects.create(user=request.user, goal=goal, value=value)
        return redirect('dashboard')
    return render(request, 'achieve_goal.html',{'goal': goal})

def leaderboard(request):
    leaderboard_data = (
        Goal.objects.values('user__username')
        .annotate(total_progress=Sum('current_value') / Sum('target_value') * 100)  # Calculate the total progress percentage
        .order_by('-total_progress')  # Sort by highest percentage
    )

    context = {
        'leaderboard_data': leaderboard_data,
    }

    return render(request, 'leaderboard.html', context)

def dashboard(request):
    goals = Goal.objects.filter(user=request.user)

    total_goals = goals.count()
    achieved_goals = goals.filter(achieved=True).count()
    in_progress_goals = total_goals - achieved_goals
    recent_achievements = Achievement.objects.filter(goal__user=request.user).order_by('-date_achieved')[:5]

    context = {
        'goals': goals,
        'total_goals': total_goals,
        'achieved_goals': achieved_goals,
        'in_progress_goals': in_progress_goals,
        'recent_achievements': recent_achievements,
    }

    return render(request, 'dashboard.html', context)
def index(request):
    return render(request, 'index.html')