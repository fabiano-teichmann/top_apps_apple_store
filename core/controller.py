import os

import pandas as pd
from django.utils.datetime_safe import datetime


class Controller(object):
    def __init__(self, file_):
        """

        Args:
            file_ (str): Path do arquivo csv que vai ser trabalhado
        """
        self.path = os.getcwd()
        now = datetime.now()
        self.csv_file = f"report_apple_store-{now.day}-{now.month}-{now.year}:{now.hour}:{now.minute}.csv"
        self. df = pd.read_csv(file_)

    def get_top_apps(self):
        """ Pega os top 10 app das categorias notícias, livros, músicas

        Returns:
            Dataframe:  10 apps de notícias com mais avaliações.
            Dataframe:  10 apps de livros com mais avaliações.
            Dataframe:  10 apps de música com mais avaliações.

        """

        # 10 apps de notícias com mais avaliações
        news = self.df[self.df.prime_genre == 'News']
        top_news = news.sort_values(by='rating_count_tot', ascending=False)

        # 10 app musicas com mais avaliações
        musics = self.df[self.df.prime_genre == 'Music']
        top_musics = musics.sort_values(by='rating_count_tot', ascending=False)

        # 10 app de livros com mais avaliações
        books = self.df[self.df.prime_genre == 'Book']
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

    def generate_array(self):
        """ Gera array numpy para salvar no banco de dados



        Returns:
            ndarray:
        """
        report = self.df[['id', 'track_name', 'rating_count_tot', 'size_bytes', 'price', 'prime_genre']]
        report = report.rename(columns={'rating_count_tot': 'n_citacoes'})
        return report.get_values()
