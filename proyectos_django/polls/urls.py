from django.urls import path

from .views import IndexView,DetailView,ResultView,vote

app_name = "polls"
urlpatterns=[
    #Ex: /polls/
    path("", IndexView.as_view(),name="index"),
    #Ex: /polls/5/
    path("<int:pk>/", DetailView.as_view(),name="detail"),
    #Ex: /polls/5/results
    #antes -> path("<int:question_id>/results/", results,name="results"),
    #ahora
    path("<int:pk>/results/", ResultView.as_view(),name="results"),
    #Ex: /polls/5/votes
    path("<int:question_id>/vote/", vote,name="vote")
]