"""...acme_project/birthday/views.py."""

from django.shortcuts import get_object_or_404, redirect, render

# Импортируем класс пагинатора.
from django.core.paginator import Paginator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .models import Birthday
from .forms import BirthdayForm
from .utils import calculate_birthday_countdown


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass


class BirthdayDetailView(DetailView):
    model = Birthday
    # template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context


# class BirthdayDeleteView(DeleteView):
    """Класс наследуемый от CBV класса DeleteView:."""

#    model = Birthday
#    success_url = reverse_lazy('birthday:list')

# class BirthdayCreateView(BirthdayMixin, CreateView):
    """Класс наследуемый от CBV класса CreateView.

    Добавляем миксин первым по списку родительских классов
    И здесь все атрибуты наследуются от BirthdayMixin.
    """

    # pass
    # Указываем модель, с которой работает CBV...
    # model = Birthday
    # Указываем имя формы:
    # form_class = BirthdayForm
    # Этот класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме:
    # fields = '__all__' # Подключились через форму!!!
    # Явным образом указываем шаблон:
    # template_name = 'birthday/birthday.html'
    # Указываем namespace:name страницы, куда будет перенаправлен
    # пользователь после создания объекта:
    # success_url = reverse_lazy('birthday:create')


# class BirthdayUpdateView(BirthdayMixin, UpdateView):
    """Класс наследуемый от CBV класса UpdateView."""

    # model = Birthday
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:create')


class BirthdayListView(ListView):
    """Класс наследуемый от CBV класса ListView:."""

    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


def birthday(request, pk=None):
    """Финкция для сохранения/редоктирования закиси в БД.

    Если присутствуетключ ключ - pk(не обязательный)
    функция используется для редактирования,
    иначе для добавления записи в БД.
    """
    if pk is not None:
        # При поиске объекта дополнительно указываем текущего пользователя.
        # instance = get_object_or_404(Birthday, pk=pk, author=request.user)

        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None

    form = BirthdayForm(
        request.POST or None,
        # Файлы, переданные в запросе, указываются отдельно.
        files=request.FILES or None,
        instance=instance
    )
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        # Форма открывается без сохранения
        instance = form.save(commit=False)
        # Присваевается автор
        instance.author = request.user
        # Сороняется.
        instance.save()
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    """Функция списка всех записей."""
    # Получаем все объекты модели Birthday из БД.
    birthdays = Birthday.objects.all().order_by('id')
    # Создаём объект пагинатора с количеством 10 записей на страницу.
    paginator = Paginator(birthdays, 10)

    # Получаем из запроса значение параметра page.
    page_number = request.GET.get('page')

    # Если параметра page нет в запросе или его значение не приводится к числу,
    # вернётся первая страница.
    page_obj = paginator.get_page(page_number)

    # Вместо полного списка объектов передаём в контекст
    # объект страницы пагинатора.
    context = {'page_obj': page_obj}
    return render(request, 'birthday/birthday_list.html', context)


def delete_birthday(request, pk):
    """Функция удаления записи по ключу pk(id)."""
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)
