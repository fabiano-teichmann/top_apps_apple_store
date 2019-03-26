import os

import pandas as pd
from django.utils.datetime_safe import datetime
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

class Controller(object):
    def __init__(self):

        self.path = os.getcwd()
        now = datetime.now()
        self.csv_file = f"report_apple_store-{now.day}-{now.month}-{now.year}:{now.hour}:{now.minute}.csv"
        client = MongoClient('localhost', 27017)
        db = client['apple_store']
        self.collection = db['apps']

    def load_csv(self, file_):
        """

        Args:
            file_ (str): path file

        Returns:

        """
        return pd.read_csv(file_)

    def get_top_apps(self, df):
        """ Pega os top 10 app das categorias notícias, livros, músicas

        Args:
            df (dataframe)
        Returns:
            Dataframe:  10 apps de notícias com mais avaliações.
            Dataframe:  10 apps de livros com mais avaliações.
            Dataframe:  10 apps de música com mais avaliações.

        """

        # 10 apps de notícias com mais avaliações
        news = df[df.prime_genre == 'News']
        top_news = news.sort_values(by='rating_count_tot', ascending=False)

        # 10 app musicas com mais avaliações
        musics = df[df.prime_genre == 'Music']
        top_musics = musics.sort_values(by='rating_count_tot', ascending=False)

        # 10 app de livros com mais avaliações
        books = df[df.prime_genre == 'Book']
        top_books = books.sort_values(by='rating_count_tot', ascending=False)
        return top_news[0:10], top_books[0:10], top_musics[0:10]

    @staticmethod
    def generate_report(top_news, top_books, top_musics):
        """ Gera o report final com os tops apps das categoria notícia, livros e musica

        Args:
            top_news (DataFrame):
            top_books (DataFrame):
            top_musics(DataFrame):

        Returns:
            DataFrame: dataframe final
        """
        # Concateno os dataframe
        df_concat = [top_news, top_books, top_musics]

        # Seleciono as colunas necessárias e renomeio rating_count_tot para n_citacoes
        report = pd.concat(df_concat)
        report = report[['id', 'track_name', 'rating_count_tot', 'size_bytes', 'price', 'prime_genre']]
        report = report.rename(columns={'rating_count_tot': 'n_citacoes'})
        return report

    def generate_csv(self, report):
        """

        Args:
            report (DataFrame):

        Returns:
            str: path csv gerado
        """
        path_file = os.path.join(self.path, 'media', self.csv_file)
        report.to_csv(path_file, index=False)
        return self.csv_file

    def save_db(self, df):
        """ Salva no mongo db os resultados

        Args:
            df (dataframe)

        Returns:
           bool:
        """

        report = df[['id', 'track_name', 'size_bytes', 'currency', 'price', 'rating_count_tot', 'rating_count_ver',
                          'user_rating', 'user_rating_ver', 'ver', 'cont_rating', 'prime_genre']]

        report = report.rename(columns={'rating_count_tot': 'n_citacoes', 'id': '_id'})

        reports = report.to_dict(orient='records')
        try:
            self.collection.insert_many(reports)
            return True
        except BulkWriteError:
            return False

    def get_all_values(self):
        data = self.collection.find({})
        return [x for x in data]
