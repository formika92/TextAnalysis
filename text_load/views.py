import json
from math import (
    log10,
)
from django.core.cache import (
    cache,
)
from django.http import (
    HttpResponse,
)
from django.views.generic import (
    TemplateView,
)
from django.views.generic.list import MultipleObjectMixin

from text_load.helpers import (
    find_all_words,
    find_word_in_document,
)
from text_load.models import (
    TextFiles,
)


class JsonResponse(HttpResponse):
    """
    Класс для отправки ответа в виде json
    """
    def __init__(self, content, **kwargs):
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(json.dumps(content), **kwargs)


class Index(TemplateView):
    template_name = 'text_load/index.html'

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('files')
        primary_key = None
        if file:
            new_file = TextFiles()
            new_file.file = file
            new_file.save()
            primary_key = new_file.pk

        return JsonResponse({'primary_key': primary_key})


class ShowFiles(
    TemplateView,
    MultipleObjectMixin,
):
    template_name = 'text_load/file.html'
    paginate_by = 5  # будем выводить по 5 строк на странице
    COUNT_STRINGS = 50
    TIME_CACHE = 60

    def get_context_data(self, pk, **kwargs):
        file_url = TextFiles.objects.get(pk=pk).file.name

        # получаем словарь с TF
        frequency_dist = find_all_words(url=file_url)

        # будем рассчитывать IDF по всем нашим документам
        # не ясно, нужно ли учитывать в расчете тот документ, который мы загружали?
        # вероятно, нет, поэтому исключаем его

        # есть различные вариации расчета IDF, пока не ясно, как рассчитывать IDF,
        # если слово уникальное, и не встречается в других документах,
        # т.к. формула https://ru.wikipedia.org/wiki/TF-IDF действительна при n(i)!=0
        # в итоге, в результат будут входить те элементы, у которых n(i)!=0
        # TODO подумать над более лучшим мехаизмом кэширования
        all_documents = cache.get(f'all_documents_{pk}')
        if not all_documents:
            all_documents = TextFiles.objects.exclude(pk=pk).values('file')
            cache.set(f'all_documents_{pk}', all_documents, self.TIME_CACHE)

        match_dict = cache.get(f'match_dict_{pk}')
        if not match_dict:
            match_dict = {}

            for document in all_documents:
                match_dict = find_word_in_document(
                    url=document.get('file'),
                    words=frequency_dist,
                    match_dict=match_dict,
                )

            cache.set(f'match_dict_{pk}', match_dict, self.TIME_CACHE)
        # посчитаем IDF
        count_documents = all_documents.count()
        for key, frequency_values in match_dict.items():
            frequency_values = sum(frequency_values)
            frequency_values = log10(count_documents/frequency_values)

            # добавим к value TF
            tf_value = frequency_dist.get(f'{key}')
            match_dict[f'{key}'] = [tf_value, frequency_values]

        # отсортируем полученный словарь по значению IDF
        sorted_match_tuples = sorted(
            match_dict.items(), key=lambda item: item[1][1],
            reverse=True
        )[:self.COUNT_STRINGS]  # будем выводить только первые 50 слов

        # sorted_match_dict = {key: value for key, value in sorted_match_tuples}
        context = super(ShowFiles, self).get_context_data(object_list=sorted_match_tuples, **kwargs)
        return context
