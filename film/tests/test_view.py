from django.test import TestCase, Client
from film.models import Movie
from film.serializers import MovieSerializer


class TestMovieViewSet(TestCase):
    def setUp(self) -> None:
        self.movie = Movie.objects.create(name="test movie", imdb=7, genre="comedy")
        self.movie = Movie.objects.create(name="test movie", imdb=10, genre="comedy")
        self.client = Client()

    def test_get_movie_list(self):
        response = self.client.get('/movies/')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertIsNotNone(data[0]['id'])
        self.assertEqual(data[0]['name'], self.movie.name)
        # self.assertEqual(data[0]['imdb'], self.movie.imdb)
        self.assertEqual(data[0]['genre'], self.movie.genre)

    def test_search_movie_list(self):
        response = self.client.get('/movies/?search=comedy')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['genre'], self.movie.genre)

    def test_filter_movie_list(self):
        response = self.client.get('/movies/?ordering=-imdb')
        data = response.data
        self.queryset = Movie.objects.all()
        objects = self.queryset.order_by('-imdb')
        serializer = MovieSerializer(objects, many=True)
        data2 = serializer.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data, data2)



