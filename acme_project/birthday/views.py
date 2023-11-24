from django.shortcuts import render

from .forms import BirthdayForm


def birthday1(request):
    # Если есть параметры GET-запроса...
    if request.GET:
        # ...передаём параметры запроса в конструктор класса формы.
        form = BirthdayForm(request.GET)
        # Если данные валидны...
        if form.is_valid():
            # ...то считаем, сколько дней осталось до дня рождения.
            pass
    # Если нет параметров GET-запроса.
    else:
        # То просто создаём пустую форму.
        form = BirthdayForm()
    context = {'form': form}
    return render(request, 'birthday/birthday.html', context)


def birthday(request):
    # тоже самое что и birthday1 но короче.
    form = BirthdayForm(request.GET or None)
    if form.is_valid():
        pass
    context = {'form': form}
    return render(request, 'birthday/birthday.html', context)
