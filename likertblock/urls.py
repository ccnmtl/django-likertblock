from django.conf.urls import patterns

urlpatterns = patterns(
    'likertblock.views',
    (r'^edit_questionnaire/(?P<id>\d+)/$', 'edit_questionnaire',
     {}, 'edit-questionnaire'),
    (r'^edit_questionnaire/(?P<id>\d+)/add_question/$',
     'add_question_to_questionnaire', {},
     'add-question-to-questionnaire'),
    (r'^edit_question/(?P<id>\d+)/$', 'edit_question', {},
     'likert-edit-question'),
    (r'^delete_question/(?P<id>\d+)/$', 'delete_question', {},
     'likert-delete-question'),
    (r'^reorder_questions/(?P<id>\d+)/$', 'reorder_questions', {},
     'likert-reorder-questions'),
)
