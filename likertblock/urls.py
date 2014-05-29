from django.conf.urls import patterns
from .views import (
    EditQuestionnaireView, DeleteQuestionView, ReorderQuestionsView)

urlpatterns = patterns(
    'likertblock.views',
    (r'^edit_questionnaire/(?P<pk>\d+)/$', EditQuestionnaireView.as_view(),
     {}, 'edit-questionnaire'),
    (r'^edit_questionnaire/(?P<pk>\d+)/add_question/$',
     'add_question_to_questionnaire', {},
     'add-question-to-questionnaire'),
    (r'^edit_question/(?P<pk>\d+)/$', 'edit_question', {},
     'likert-edit-question'),
    (r'^delete_question/(?P<pk>\d+)/$', DeleteQuestionView.as_view(), {},
     'likert-delete-question'),
    (r'^reorder_questions/(?P<pk>\d+)/$', ReorderQuestionsView.as_view(), {},
     'likert-reorder-questions'),
)
