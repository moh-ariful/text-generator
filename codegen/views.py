from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import openai
from .models import Answer
from django.views.generic import View
from django.db.models import Q


openai.api_key = ''

@login_required
def index(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt')
        model_engine = "text-davinci-002"

        try:
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=4000,
                n=1,
                temperature=0.5,
            )
            # Create an Answer object and save it to the database
            answer = Answer(user=request.user, tanya=prompt, jawab=completions.choices[0].text)
            answer.save()
        except openai.errors.OpenAiError as e:
            error_message = "Error: {}".format(e)
            return render(request, "index.html", {'error_message': error_message})

        message = completions.choices[0].text
        return render(request, "index.html", {'message': message})
    else:
        return render(request, 'index.html')


class SearchView(View):

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        error_message = ""
        query_list = None
        if not query:
             error_message = "Error: No query entered"
        else:
            if request.user.is_authenticated:
                query_list = Answer.objects.filter(
                    Q(tanya__icontains=query) |
                    Q(jawab__icontains=query)
                    )
            else:
                 error_message = "Error: User not authenticated"

        context = {
            'error_message': error_message,
            'query_list': query_list,
        }

        return render(request, 'search.html', context)
