from datetime import datetime, timedelta
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, Http404


def hello_world(request):
    return HttpResponse('Hello World')


def current_date(request):
    try:
        str_format = '%d, %B %Y'
        current_date_today = datetime.now().strftime(str_format)
    except ValueError:
        raise Http404
    return HttpResponse(f'Today is {current_date_today}')


def my_age(request, year, month, day):
    current_year = datetime.now().year
    my_age_format = current_year - year
    return HttpResponse(f'Your age is {my_age_format} years old')


def next_birthday(request, birthday):
    try:
        str_format = '%Y-%m-%d'
        birthday = datetime.strptime(birthday, str_format)
        # print('birthday is :', birthday)
    except ValueError:
        return HttpResponseBadRequest()

    today = datetime.now()

    nextBirthdayYear = birthday.replace(year=today.year) # override my birthday with current year
    # print('next birthday for year is :', nextBirthdayYear)
    if today > birthday:
        nextBirthdayYear = nextBirthdayYear.replace(year=today.year + 1)
    else:
        nextBirthdayYear = nextBirthdayYear.replace(year=today.year)

    diff =  nextBirthdayYear - today
    return HttpResponse(f'Days until next birthday: {diff.days}')


def profile(request):
    context = {
        'my_name':'AZGHOUR',
        'my_age': 26
    }
    return render(request, 'profile.html', context)



"""
    The goal for next task is to practice routing between two URLs.
    You will have:
        - /authors --> contains a list of Authors (template is provided to you)
        - /author/<authors_last_name> --> contains the detail for given author,
        using the AUTHORS_INFO provided below.

    First view just have to render the given 'authors.html' template sending the
    AUTHORS_INFO as context.

    Second view has to take the authors_last_name provided in the URL, look for
    the proper author info in the dictionary, and send it as context while
    rendering the 'author.html' template. Make sure to complete the given
    'author.html' template with the data that you send.
"""
AUTHORS_INFO = {
    'poe': {
        'full_name': 'Edgar Allan Poe',
        'nationality': 'US',
        'notable_work': 'The Raven',
        'born': 'January 19, 1809',
    },
    'borges': {
        'full_name': 'Jorge Luis Borges',
        'nationality': 'Argentine',
        'notable_work': 'The Aleph',
        'born': 'August 24, 1899',
    }
}

def authors(request):
    context = {
        'authors': AUTHORS_INFO
    }
    return render(request, 'authors.html', context)


def author(request, authors_last_name):
    if authors_last_name in AUTHORS_INFO:
        return render(request, 'author.html', AUTHORS_INFO[authors_last_name])
    return redirect(reverse('authors'))   # Getting 'authors' from url's name