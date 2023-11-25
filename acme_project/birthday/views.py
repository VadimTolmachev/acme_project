from django.shortcuts import render

from .forms import BirthdayForm
from .utils import calculate_birthday_countdown


def birthday1(request):
    # Если есть параметры GET-запроса...
    if request.GET:
        # ...передаём параметры запроса в конструктор класса формы.
        form = BirthdayForm(request.GET)
    # Если нет параметров GET-запроса.
    else:
        # То просто создаём пустую форму.
        form = BirthdayForm()
    context = {'form': form}

    # Если данные валидны...
    if form.is_valid():
        # ...то считаем, сколько дней осталось до дня рождения.
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


def birthday(request):
    # тоже самое что и birthday1 но короче.
    form = BirthdayForm(request.GET or None)
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)
