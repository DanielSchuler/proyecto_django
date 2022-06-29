from django.urls import path

from .views import index,detail,results,vote

app_name = "polls"
urlpatterns=[
    #Ex: /polls/
    path("", index,name="index"),
    #Ex: /polls/5/
    path("<int:question_id>/", detail,name="detail"),
    #Ex: /polls/5/results
    path("<int:question_id>/results/", results,name="results"),
    #Ex: /polls/5/votes
    path("<int:question_id>/vote/", vote,name="vote")
]