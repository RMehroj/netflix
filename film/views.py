from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.transaction import atomic
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.models import User
from rest_framework import filters
from django.contrib.postgres.search import TrigramSimilarity
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.decorators import api_view

from film.models import (Movie,
                         Actor,
                         Comment,
                         Account)

from film.serializers import (
    MovieSerializer,
    ActorSerializer,
    CommentSerializer,
    RegistrationSerializer,
)


@api_view(['POST'])
def registration_view(request):
    email = request.data.get('email')
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid(raise_exception=True):
            account = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
        return Response(data)

    return Response({'message': 'Account with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)


class MovieViewSet(ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # filter_backends = [filters.DjangoFilterBackend,]
    # filterset_fields = ['genre', 'id',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['-imdb', 'imdb']

    def get_queryset(self):
        queryset = Movie.objects.all()
        query = self.request.query_params.get('search')
        if query is not None:
            queryset =queryset.annotate(
                similarity=TrigramSimilarity('genre', query)
            ).filter(similarity__gt=0.3).order_by('-similarity')
        return queryset

    @action(detail=True, methods=['post'])
    def add_actor(self, request, pk=None):
        movie = self.get_object()
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid():
            actor = serializer.save()
            movie.actor.add(actor)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remove_actor(self, request, pk=None):
        movie = self.get_object()
        actor = request.data.get('actor')
        movie.actor.remove(actor)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActorVievSet(ReadOnlyModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieActorAPIView(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        actors = movie.actor.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)


#For a user who has a token, add a comment and create
# an ApiView that returns a list of coments.
class CommentListCreate(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user_id=self.request.user)


#Create an ApiView to add a comment for a user who has a token
class CommentPost(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        comment = serializer.save()
        return Response(data=serializer.data)

#Create an ApiView that returns a list of comment for the user who has the token.
# class CommentGet(generics.ListCreateAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = CommentSerializer
#
#     def get(self, request):
#         comments = Comment.objects.filter(user_id=self.request.user)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(data=serializer.data)


class CommentDelete(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        comment = request.data.get('comment')
        Comment.objects.get(pk=comment).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
