import json
from datetime import date

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from SpendingsApp.models import Category, Spending

User = get_user_model()


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class HomePageAuthenticationIntegrationTest(SimpleTestCase):
    def test_home_redirects_to_login_when_user_is_not_logged_in(self):
        response = self.client.get(reverse("home"))

        expected_login_url = f"{reverse('login')}?next={reverse('home')}"
        self.assertRedirects(
            response,
            expected_login_url,
            status_code=302,
            target_status_code=200,
        )


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class HomePageRecentSpendingsIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.category = Category.objects.create(name="Groceries", user=self.user)

        self.spending1 = Spending.objects.create(
            spendingDate=date(2026, 1, 1),
            description="Supermarket",
            amount=42.50,
            category=self.category,
            user=self.user,
        )
        self.spending2 = Spending.objects.create(
            spendingDate=date(2026, 1, 2),
            description="Bakery",
            amount=5.00,
            category=self.category,
            user=self.user,
        )
        self.spending3 = Spending.objects.create(
            spendingDate=date(2026, 1, 3),
            description="Pharmacy",
            amount=18.90,
            category=self.category,
            user=self.user,
        )


    def test_home_page_returns_200_when_logged_in(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recently submitted")


    def test_recent_spendings_api_returns_all_three_spendings(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(
            reverse("spending_get_recent"), data={"count": 10}
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        returned_descriptions = {s["description"] for s in data["spendings"]}
        self.assertEqual(
            returned_descriptions,
            {"Supermarket", "Bakery", "Pharmacy"},
        )


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class HomePageRecentSpendingsOtherUserTest(TestCase):
    USERNAME_1 = "testuser1"
    PASSWORD_1 = "testpass123"
    USERNAME_2 = "testuser2"
    PASSWORD_2 = "testpass123"

    def setUp(self):
        self.user1 = User.objects.create_user(
            username=self.USERNAME_1,
            password=self.PASSWORD_1,
        )
        self.user2 = User.objects.create_user(
            username=self.USERNAME_2,
            password=self.PASSWORD_2,
        )

        self.category1 = Category.objects.create(name="Groceries", user=self.user1)
        self.category2 = Category.objects.create(name="Utilities", user=self.user2)

        self.spending1 = Spending.objects.create(
            spendingDate=date(2026, 1, 1),
            description="Supermarket",
            amount=42.50,
            category=self.category1,
            user=self.user1,
        )
        self.spending2 = Spending.objects.create(
            spendingDate=date(2026, 1, 1),
            description="Supermarket",
            amount=42.50,
            category=self.category2,
            user=self.user2,
        )

    def test_recentSpendingsApi_returnsOnlySpendingsForLoggedInUser(self):
        self.client.login(username=self.USERNAME_1, password=self.PASSWORD_1)

        response = self.client.get(
            reverse("spending_get_recent"), data={"count": 10}
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        returned_descriptions = {s["description"] for s in data["spendings"]}
        self.assertEqual(
            returned_descriptions,
            {"Supermarket"},
        )
