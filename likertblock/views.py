from .models import Questionnaire, Question
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse


def edit_questionnaire(request, id):
    questionnaire = get_object_or_404(Questionnaire, id=id)
    section = questionnaire.pageblock().section
    return render(
        request,
        'likertblock/edit_questionnaire.html',
        dict(questionnaire=questionnaire, section=section))


def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        questionnaire = question.questionnaire
        question.delete()
        return HttpResponseRedirect(
            reverse("edit-questionnaire", args=[questionnaire.id]))
    return HttpResponse("""
<html><body><form action="." method="post">Are you Sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")


def reorder_questions(request, id):
    if request.method != "POST":
        return HttpResponse("only use POST for this", status=400)
    questionnaire = get_object_or_404(Questionnaire, id=id)
    keys = request.GET.keys()
    question_keys = [int(k[len('question_'):]) for k in keys
                     if k.startswith('question_')]
    question_keys.sort()
    questions = [int(request.GET['question_' + str(k)]) for k in question_keys]
    questionnaire.update_questions_order(questions)
    return HttpResponse("ok")


def add_question_to_questionnaire(request, id):
    questionnaire = get_object_or_404(Questionnaire, id=id)
    form = questionnaire.add_question_form(request.POST)
    if form.is_valid():
        question = form.save(commit=False)
        question.questionnaire = questionnaire
        question.save()
    return HttpResponseRedirect(
        reverse("edit-questionnaire", args=[questionnaire.id]))


def edit_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        form = question.edit_form(request.POST)
        question = form.save(commit=False)
        question.save()
        return HttpResponseRedirect(reverse("likert-edit-question",
                                            args=[question.id]))
    return render(
        request,
        'likertblock/edit_question.html',
        dict(question=question))
