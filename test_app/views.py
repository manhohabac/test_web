from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import csv
import random
import io
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required


class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.side_up = "Q"


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'test_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'test_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'test_app/home.html')


def start_test(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = io.TextIOWrapper(csv_file, encoding='utf-8')
        flashcards = get_flashcards(decoded_file)
        request.session['flashcards'] = [(f.question, f.answer) for f in flashcards]
        request.session['current_index'] = 0
        request.session['displayed_questions'] = []
        return redirect('test')

    return render(request, 'test_app/start_test.html')


def get_flashcards(file):
    flashcard_list = []
    reader = csv.reader(file)
    next(reader, None)  # Skip header
    for line in reader:
        flashcard_list.append(Flashcard(line[0], line[1]))
    return flashcard_list


def test_view(request):
    if 'flashcards' not in request.session:
        return redirect('start_test')

    flashcards = [Flashcard(q, a) for q, a in request.session['flashcards']]
    if 'displayed_questions' not in request.session:
        request.session['displayed_questions'] = []
    if 'current_index' not in request.session:
        request.session['current_index'] = 0

    displayed_questions = request.session.get('displayed_questions', [])
    current_index = request.session.get('current_index', 0)

    if not displayed_questions:
        selected_question = flashcards[current_index]
        displayed_questions.append(selected_question.question)
        request.session['displayed_questions'] = displayed_questions
        request.session['current_index'] = 0

    current_card = flashcards[current_index]

    context = {
        'current_card': current_card,
        'card_index': current_index,
        'total_cards': len(flashcards),
        'questions_remaining': len(flashcards) - len(displayed_questions)
    }

    return render(request, 'test_app/test.html', context)


def flip_view(request):
    flashcards = [Flashcard(q, a) for q, a in request.session['flashcards']]
    current_index = request.session['current_index']
    flashcard = flashcards[current_index]
    flashcard.side_up = "A" if flashcard.side_up == "Q" else "Q"
    request.session['flashcards'] = [(f.question, f.answer) for f in flashcards]
    return redirect('test')


def next_card_view(request):
    flashcards = [Flashcard(q, a) for q, a in request.session['flashcards']]
    displayed_questions = request.session.get('displayed_questions', [])
    current_index = request.session.get('current_index', 0)

    print('current index', current_index)
    print('len(flashcards)', len(flashcards))

    # Check if all questions have been displayed
    if current_index >= len(flashcards):
        return JsonResponse({'status': 'no_more_questions', 'question': None, 'answer': None})

    current_card = flashcards[current_index]
    if current_card.question not in displayed_questions:
        displayed_questions.append(current_card.question)
        request.session['displayed_questions'] = displayed_questions
    else:
        # If current question is already displayed, find the next non-displayed question
        while current_card.question in displayed_questions and current_index < len(flashcards) - 1:
            current_index += 1
            current_card = flashcards[current_index]
        if current_card.question in displayed_questions:
            return JsonResponse({'status': 'no_more_questions', 'question': None, 'answer': None})
        displayed_questions.append(current_card.question)
        request.session['displayed_questions'] = displayed_questions

    current_index += 1
    request.session['current_index'] = current_index

    return JsonResponse({'status': 'ok', 'question': current_card.question, 'answer': current_card.answer})


def prev_card_view(request):
    current_index = request.session.get('current_index', 0)
    if current_index > 0:
        current_index -= 1
    request.session['current_index'] = current_index

    flashcards = [Flashcard(q, a) for q, a in request.session['flashcards']]
    current_card = flashcards[current_index]
    return JsonResponse({'question': current_card.question, 'answer': current_card.answer})


def check_answer_view(request):
    if request.method == 'POST':
        user_answer = request.POST['answer'].strip()
        flashcards = [Flashcard(q, a) for q, a in request.session['flashcards']]
        card_index = request.session['current_index']
        correct_answer = flashcards[card_index].answer.strip()
        result = "Correct!" if user_answer.lower() == correct_answer.lower() else f"Incorrect! The answer is: {correct_answer}"
        return JsonResponse({'result': result})
    return redirect('test')


def result_page(request):
    user = request.user
    score = request.session.get('user_score', 0)
    context = {'user': user, 'score': score}

    return render(request, 'test_app/result_page.html', context)