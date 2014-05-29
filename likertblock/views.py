from .models import Questionnaire, Question
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView


class EditQuestionnaireView(DetailView):
    model = Questionnaire


class DeleteQuestionView(View):
    def get(self, request, pk, **kwargs):
        return HttpResponse("""
        <html><body><form action="." method="post">Are you Sure?
        <input type="submit" value="Yes, delete it" /></form></body></html>
        """)

    def post(self, request, pk, **kwargs):
        question = get_object_or_404(Question, pk=pk)
        questionnaire = question.questionnaire
        question.delete()
        return HttpResponseRedirect(
            reverse("edit-questionnaire", args=[questionnaire.id]))


class ReorderQuestionsView(View):
    def post(self, request, pk):
        questionnaire = get_object_or_404(Questionnaire, pk=pk)
        keys = request.GET.keys()
        question_keys = [int(k[len('question_'):]) for k in keys
                         if k.startswith('question_')]
        question_keys.sort()
        questions = [int(request.GET['question_' + str(k)])
                     for k in question_keys]
        questionnaire.update_questions_order(questions)
        return HttpResponse("ok")


class AddQuestionToQuestionnaireView(View):
    def post(self, request, pk):
        questionnaire = get_object_or_404(Questionnaire, pk=pk)
        form = questionnaire.add_question_form(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.questionnaire = questionnaire
            question.save()
        return HttpResponseRedirect(
            reverse("edit-questionnaire", args=[questionnaire.id]))


class EditQuestionView(View):
    template_name = 'likertblock/edit_question.html'

    def get_object(self, pk):
        return get_object_or_404(Question, pk=pk)

    def get(self, request, pk):
        return render(
            request,
            self.template_name,
            dict(question=self.get_object(pk)))

    def post(self, request, pk):
        question = self.get_object(pk)
        form = question.edit_form(request.POST)
        question = form.save(commit=False)
        question.save()
        return HttpResponseRedirect(reverse("likert-edit-question",
                                            args=[question.id]))
