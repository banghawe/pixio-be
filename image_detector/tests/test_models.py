import datetime

from django.test import TestCase
from image_detector.models import Plan, Subscription
from django.contrib.auth.models import User


class PlanModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Plan.objects.create(name="Free", price=0, status=1)
        Plan.objects.create(name="Premium", price=1000, status=0)

    def test_object_name_is_name(self):
        plan = Plan.objects.get(id=1)
        expected_object_name = plan.name
        self.assertEqual(str(plan), expected_object_name)

    def test_only_get_active_plan(self):
        first_plan = Plan.objects.get(id=1)
        second_plan = Plan.objects.get(id=2)
        plans = Plan.active_objects.all()
        self.assertEqual(True, first_plan in plans)
        self.assertEqual(False, second_plan in plans)


class SubscriptionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        plan = Plan.objects.create(name="Free", price=0, status=1)
        user = User.objects.create_user(
            username="alpha",
            password="12345678!",
            email="alpha@site.com"
        )
        Subscription.objects.create(
            username=user,
            plan=plan,
            end_at=None,
            status=0
        )
        Subscription.objects.create(
            username=user,
            plan=plan,
            start_at=datetime.date.today() - datetime.timedelta(days=2),
            end_at=datetime.date.today() - datetime.timedelta(days=1),
            status=1
        )
        Subscription.objects.create(
            username=user,
            plan=plan,
            end_at=None,
            status=1
        )

    def test_is_active_for_false_status(self):
        subs = Subscription.objects.get(id=1)
        self.assertEqual(False, subs.is_active())

    def test_is_active_for_end_at_lesser_than_today(self):
        subs = Subscription.objects.get(id=2)
        self.assertEqual(False, subs.is_active())

    def test_is_active_for_true_status_end_at_none(self):
        subs = Subscription.objects.get(id=3)
        self.assertEqual(True, subs.is_active())

    def test_object_name_is_plan_hyphen_is_active(self):
        first_sub = Subscription.objects.get(id=1)
        second_sub = Subscription.objects.get(id=2)
        third_sub = Subscription.objects.get(id=3)

        self.assertEqual(str(first_sub), f'{first_sub.plan} - {first_sub.is_active()}')
        self.assertEqual(str(second_sub), f'{second_sub.plan} - {second_sub.is_active()}')
        self.assertEqual(str(third_sub), f'{third_sub.plan} - {third_sub.is_active()}')

    def test_only_get_active_subscription(self):
        first_sub = Subscription.objects.get(id=1)
        second_sub = Subscription.objects.get(id=2)
        third_sub = Subscription.objects.get(id=3)
        subs = Subscription.active_objects.all()

        self.assertEqual(False, first_sub in subs)
        self.assertEqual(False, second_sub in subs)
        self.assertEqual(True, third_sub in subs)

    def test_deactivate(self):
        active_sub = Subscription.objects.get(id=3)
        active_sub.deactivate()
        subs = Subscription.objects.get(id=3)

        self.assertEqual(False, subs.status)

