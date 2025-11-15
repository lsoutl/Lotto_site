from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone
from django.contrib.auth import get_user_model
from lotto.models import Draw, Ticket

User = get_user_model()

class TestCommands(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")

    def test_draw_lotto_creates_winning_numbers(self):
        d = Draw.objects.create(number=101, draw_date=timezone.now().date(), status="SCHEDULED")
        call_command("draw_lotto", 101)
        d.refresh_from_db()
        self.assertEqual(d.status, "DONE")
        self.assertIsInstance(d.winning_numbers, list)
        self.assertEqual(len(d.winning_numbers), 6)

    def test_settle_lotto_scores_tickets(self):
        d = Draw.objects.create(number=102, draw_date=timezone.now().date(), status="DONE",
                                winning_numbers=[1,2,3,4,5,6])
        # 1등, 3등, 꽝 하나씩
        Ticket.objects.create(user=self.user, draw=d, is_auto=False, picks=[1,2,3,4,5,6])
        Ticket.objects.create(user=self.user, draw=d, is_auto=False, picks=[1,2,3,4,40,41])
        Ticket.objects.create(user=self.user, draw=d, is_auto=False, picks=[7,8,9,10,11,12])

        call_command("settle_lotto", 102)

        ranks = list(Ticket.objects.order_by("purchased_at").values_list("rank", flat=True))
        self.assertCountEqual(ranks, [1, 3, 0])