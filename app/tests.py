from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy

from app.models import Content, UserScoreContent


class ContentModelTest(TestCase):
    def setUp(self):
        self.url = reverse('content_list')
        self.user = mommy.make(User)
        self.content = mommy.make(Content)

    def test_scores_stat(self):
        scores = [1, 2, 3]
        mommy.make(UserScoreContent, score=scores[0], content=self.content)
        mommy.make(UserScoreContent, score=scores[1], content=self.content)
        mommy.make(UserScoreContent, score=scores[2], content=self.content)

        self.assertEqual(self.content.scores_stat['sum_scores'], sum(scores))
        self.assertEqual(self.content.scores_stat['mean_scores'], sum(scores)/len(scores))


class UserContentScoreUpdateCreateApiviewTest(APITestCase):
    def setUp(self):
        self.url = reverse('add_content_score')
        self.user = mommy.make(User)
        self.content = mommy.make(Content)
        self.client.force_authenticate(self.user)

    def test_create_score_for_content(self):
        score = 2
        response = self.client.post(self.url, data={"content": self.content.id, "score": score})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_score_content = UserScoreContent.objects.get(
            user=self.user,
            content=self.content
        )
        self.assertIsNotNone(user_score_content)
        self.assertEqual(user_score_content.score, score)

    def test_update_score_for_content(self):
        old_score = 1
        user_score_content = UserScoreContent.objects.create(
            user=self.user,
            content=self.content,
            score=old_score
        )
        new_score = 2
        response = self.client.post(self.url, data={"content": self.content.id, "score": new_score})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_score_content.refresh_from_db()
        self.assertIsNotNone(user_score_content)
        self.assertEqual(user_score_content.score, new_score)


class ContentListApiviewTest(APITestCase):
    def setUp(self):
        self.url = reverse('content_list')
        self.user = mommy.make(User)
        content = mommy.make(Content)
        mommy.make(UserScoreContent, score=1, content=content)
        mommy.make(UserScoreContent, score=5, content=content)
        self.client.force_authenticate(self.user)

    def test_get_content_list_user_score_stat_field(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['scores_stat']['mean_scores'], 3)
        self.assertEqual(response.data[0]['scores_stat']['sum_scores'], 6)

    def test_get_content_list_user_score_field(self):
        content = mommy.make(Content)
        mommy.make(UserScoreContent, score=3, user=self.user, content=content)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data[0]['user_score'])
        self.assertEqual(response.data[1]['user_score'], 3)
