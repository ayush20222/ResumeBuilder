from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import LoginForm
from .models import UserProfile
from .utils import preprocess_text, get_job_recommendations, load_job_profiles
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('resumebuild')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def job_recommendations(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    resume_text = user_profile.resume_content
    file_path = 'home/data/job_profiles.xlsx'  
    job_profiles = load_job_profiles(file_path)
    recommendations = get_job_recommendations(resume_text, job_profiles)
    
    return render(request, 'job_recommendations.html', {'recommendations': recommendations})

def index_view(request): 
	if request.method == 'POST': 
		name = request.POST.get('name', '') 
		about = request.POST.get('about', '') 
		age = request.POST.get('age', '') 
		email = request.POST.get('email', '') 
		phone = request.POST.get('phone', '') 
		skills = []
		for key in request.POST:
			if key.startswith('skill'):
				skills.append(request.POST[key])
		education_data = []
		for i in range(1,6):
			degree = request.POST.get(f'degree{i}','')
			college = request.POST.get(f'college{i}', '')
			year = request.POST.get(f'year{i}', '')
			if degree and college and year:
				education_data.append({
                    'degree': degree,
                    'college': college,
                    'year': year
                }) 
		projects = []
		for i in range(1, 6):   
			title = request.POST.get(f'project{i}_title')
			duration = request.POST.get(f'project{i}_duration')
			desc = request.POST.get(f'project{i}_desc')
			if title and duration and desc:	
				projects.append({'title': title, 'duration': duration, 'description': desc})
		experience = []
		for i in range(1, 11):
			company = request.POST.get(f'company{i}')
			post = request.POST.get(f'post{i}')
			duration = request.POST.get(f'duration{i}')
			description = request.POST.get(f'description{i}')
			if company and post and duration and description:
				experience.append({'company': company, 'post': post, 'duration': duration, 'description': description})
		achievements = []
		for i in range(1, 6):
			achievement = request.POST.get(f'ach{i}')
			if achievement:
				achievements.append(achievement)
        
		languages = []
		for i in range(1, 7):
			language = request.POST.get(f'lang{i}')
			if language:
				languages.append(language)

		resume_content = f"Name: {name}\nAbout: {about}\nAge: {age}\nEmail: {email}\nPhone: {phone}\n" \
                         f"Skills: {', '.join(skills)}\nEducation: {education_data}\nProjects: {projects}\n" \
                         f"Experience: {experience}\nAchievements: {achievements}\nLanguages: {languages}"
        
		if request.user.is_authenticated:
			user_profile, created = UserProfile.objects.get_or_create(user=request.user)
			user_profile.resume_content = resume_content
			user_profile.save()

		return render(request, 'resume.html', {'name':name, 
											'about':about,  
											'age':age, 'email':email, 
											'phone':phone, 'skills':skills, 
											'education_data': education_data,'languages':languages,
											'projects':projects,'experience':experience,'achievements':achievements}) 
	
	return render(request, 'index.html') 
