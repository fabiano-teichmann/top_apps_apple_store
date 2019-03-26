import os
from json import dumps

from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from django.core.files.storage import FileSystemStorage
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
            file_, save = self.report(url)
            uploaded_file_url = fs.url(file_)
            if save:
                return render(request, self.template_name, {
                    'uploaded_file_url': uploaded_file_url, 'msg': 'Salvo com sucesso'
                })
            else:
                return render(request, self.template_name, {
                    'uploaded_file_url': uploaded_file_url,
                    'msg': 'Este arquivo csv já esta inserido no banco de daodos'})

        return render(request, self.template_name, {'msg': None})

    def report(self, url):
        controller = Controller()
        df = controller.load_csv(file_=url)
        news, books, musics = controller.get_top_apps(df)
        report = controller.generate_report(top_news=news, top_books=books, top_musics=musics)
        file_ = controller.generate_csv(report)
        save = controller.save_db(df)
        return file_, save


class ReturnJsonView(generic.DetailView):
    model = AppsAppleStore

    def get(self, request):
        data = Controller().get_all_values()
        data = {"data": dumps(data)}
        return JsonResponse(data)
