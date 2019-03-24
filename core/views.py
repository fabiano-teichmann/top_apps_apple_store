import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from django.core.files.storage import FileSystemStorage
from django.core import serializers

from core.controller import Controller
from core.models import AppsAppleStore


class HomeView(generic.CreateView):
    template_name = 'home.html'
    model = AppsAppleStore

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST' and request.FILES['csv']:
            myfile = request.FILES['csv']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            base = os.getcwd()
            url = os.path.join(base, 'media', filename)
            file_, df = self.report(url)
            uploaded_file_url = fs.url(file_)
            #self.save_db(tops=df)

            return render(request, self.template_name, {
                'uploaded_file_url': uploaded_file_url
            })
        return render(request, self.template_name)

    def report(self, url):
        controller = Controller(file_=url)
        news, books, musics = controller.get_top_apps()
        report = controller.generate_report(top_news=news, top_books=books, top_musics=musics)
        file_ = controller.generate_csv(report)
        tops = controller.generate_array()
        return file_, tops

    def save_db(self, tops):
        for i in tops:
            self.model.objects.create(id=i[0], track_name=i[1], n_citacoes=i[2],
                                      size_bytes=i[3], price=i[4], prime_genre=i[5])


class ReturnJsonView(generic.DetailView):
    model = AppsAppleStore

    def get(self, request):
        SomeModel_json = serializers.serialize("json", AppsAppleStore.objects.all())
        data = {"SomeModel_json": SomeModel_json}
        return JsonResponse(data)
