from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import datetime
from film.models import Movie, Actor, Comment
from film.models import Account


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError('Passwords must match')
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return super().create(validated_data)


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ('name', 'birthdate', 'gender',)

    def validate(self, value):

        if value["birthdate"] < datetime.date(1950, 1, 1):
            raise ValidationError(detail="Enter a valid birthdate.")

        return value


class MovieSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'year', 'imdb', 'genre', 'actor',)


class CommentSerializer(serializers.ModelSerializer):
    # user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('movie_id', 'user_id', 'text', 'created_date',)
