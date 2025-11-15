from django.test import SimpleTestCase
from lotto import services

class TestQuickPick(SimpleTestCase):
    def test_quick_pick_basic(self):
        nums = services.quick_pick()
        self.assertIsInstance(nums, list)
        self.assertEqual(len(nums), 6)
        self.assertEqual(len(nums), len(set(nums)))  # 중복 없음
        self.assertTrue(all(1 <= n <= 45 for n in nums))
        self.assertEqual(nums, sorted(nums))  # 정렬된 상태

class TestScore(SimpleTestCase):
    def test_score_ranks(self):
        winning = [1,2,3,4,5,6]
        self.assertEqual(services.score([1,2,3,4,5,6], winning), {"match_count": 6, "rank": 1})
        self.assertEqual(services.score([1,2,3,4,5,7], winning), {"match_count": 5, "rank": 2})
        self.assertEqual(services.score([1,2,3,4,7,8], winning), {"match_count": 4, "rank": 3})
        self.assertEqual(services.score([1,2,3,7,8,9], winning), {"match_count": 3, "rank": 4})
        self.assertEqual(services.score([1,2,7,8,9,10], winning), {"match_count": 2, "rank": 0})