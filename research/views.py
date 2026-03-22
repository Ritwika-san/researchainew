from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .ai_service import research_topic
from .models import ResearchQuery

@login_required
def home(request):
    return render(request, 'research/home.html')
    return render(request, 'research/home.html', {'queries': queries})

@login_required
def research(request):
    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()
        
        if not topic:
            return JsonResponse({'error': 'Please enter a topic'}, status=400)
        
        result = research_topic(topic)
        
        query = ResearchQuery.objects.create(
            user=request.user,
            topic=topic,
            result=result
        )
        
        return JsonResponse({
            'success': True,
            'topic': topic,
            'result': result,
            'id': query.id
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
