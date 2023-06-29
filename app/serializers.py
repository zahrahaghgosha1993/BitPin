from rest_framework import serializers

from app.models import UserScoreContent, Content


class UserScoreContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScoreContent
        fields = ('score', 'content')

    def save(self, **kwargs):
        self.validated_data['user'] = self.context['request'].user
        instance = UserScoreContent.objects.filter(
            user=self.validated_data['user'],
            content=self.validated_data['content']
        ).first()
        if instance:  # if instance exist automatically .save() calls update method.
            self.instance = instance
        return super().save()


class ScoreStatSerializer(serializers.Serializer):
    mean_scores = serializers.FloatField()
    sum_scores = serializers.IntegerField()


class ContentListSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()
    scores_stat = ScoreStatSerializer()

    class Meta:
        model = Content
        fields = ('id', 'title', 'description', 'scores_stat', 'user_score')

    def get_user_score(self, obj):
        user = self.context['request'].user
        try:
            return UserScoreContent.objects.get(
                user=user,
                content=obj
            ).score
        except UserScoreContent.DoesNotExist:
            return None
