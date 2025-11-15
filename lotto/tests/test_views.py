from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from lotto.models import Draw, Ticket

User = get_user_model()

class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.draw = Draw.objects.create(number=201, draw_date=timezone.now().date(), status="SCHEDULED")

    def test_index(self):
        resp = self.client.get(reverse("index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "로또")  # 템플릿에 맞게 적당히 키워드 확인

    def test_buy_auto_requires_login(self):
        resp = self.client.get(reverse("buy_auto", args=[self.draw.number]))
        self.assertEqual(resp.status_code, 302)  # 로그인 리다이렉트

    def test_buy_auto_success(self):
        self.client.login(username="u", password="p")
        resp = self.client.get(reverse("buy_auto", args=[self.draw.number]))
        self.assertEqual(resp.status_code, 302)  # my_tickets로 리다이렉트
        self.assertEqual(Ticket.objects.filter(user=self.user, draw=self.draw).count(), 1)

    def test_buy_manual_success(self):
        self.client.login(username="u", password="p")
        resp = self.client.post(reverse("buy_manual", args=[self.draw.number]), {
            "numbers": "1,3,12,21,33,42"
        })
        self.assertEqual(resp.status_code, 302)
        t = Ticket.objects.filter(user=self.user, draw=self.draw).latest("purchased_at")
        self.assertEqual(t.picks, [1,3,12,21,33,42])