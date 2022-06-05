from django.contrib.auth import get_user
from django.urls import reverse

from django.test import TestCase
from  users.models import CustomUser



class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username":"xurshid",
                "first_name":"xurshid",
                "last_name":"olimov",
                "email":"xurshidolimov017@gmail.com",
                "password":"turkiston"
            }
        )

        user=CustomUser.objects.get(username="xurshid")

        self.assertEqual(user.first_name, "xurshid")
        self.assertEqual(user.last_name, "olimov")
        self.assertEqual(user.email, "xurshidolimov017@gmail.com")
        self.assertNotEqual(user.password, "turkiston")
        self.assertTrue(user.check_password("turkiston"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name":"xurshid",
                "email":"xurshidolimov017@gmail.com"
            }
        )

        user_count=CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response=self.client.post(
            reverse("users:register"),
            data={
                "username": "xurshid",
                "first_name": "xurshid",
                "last_name": "olimov",
                "email": "invalid-email",
                "password": "turkiston"
            }
        )
        user_count=CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user=CustomUser.objects.create(username="xurshid", first_name="xurshid")
        user.set_password("turkiston")
        user.save()



        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "xurshid",
                "first_name": "xurshid",
                "last_name": "olimov",
                "email": "xurshidolimov017@gmail.com",
                "password": "turkiston"
            }
        )




        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)

        self.assertFormError(response, "form", "username", "A user with that username already exists.")



class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="xurshid", first_name="xurshid")
        self.db_user.set_password("turkiston")
        self.db_user.save()

    def test_seccesful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username":"xurshid",
                "password":"turkiston"
            }
        )

        user=get_user(self.client)

        self.assertTrue(user.is_authenticated)


    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username":"wrong-user",
                "password":"turkiston"
            }
        )
        user=get_user(self.client)
        self.assertFalse(user.is_authenticated)




        self.client.post(
            reverse("users:login"),
            data={
                "username":"xurshid",
                "password":"wrong-password"
            }
        )
        user=get_user(self.client)
        self.assertFalse(user.is_authenticated)


    def test_logout(self):
        self.client.login(username="xurshid", password="turkiston")

        self.client.get(reverse("users:logout"))

        user=get_user(self.client)
        self.assertFalse(user.is_authenticated)




class ProfileTestCase(TestCase):
    def test_login_required(self):
        response=self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login")+"?next=/users/profile/")


    def test_profile_details(self):
        user=CustomUser.objects.create(
            username="xurshid", first_name="xurshid", last_name="olimov", email="xurshidolimov017@gmail.com"
        )

        user.set_password("turkiston")
        user.save()

        self.client.login(username="xurshid", password="turkiston")

        response=self.client.get(reverse("users:profile"))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)


    def test_update_profile(self):
        user=CustomUser.objects.create(
            username="xurshid", first_name="xurshid", last_name="olimov", email="xurshidolimov017@gmail.com"
        )

        user.set_password("turkiston")
        user.save()

        self.client.login(username="xurshid", password="turkiston")

        response=self.client.post(
            reverse("users:profile-edit"),
            data={
                "username":"xurshid",
                "first_name":"xurshid",
                "last_name":"olimovv",
                "email":"bek@go.com"
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, "olimovv")
        self.assertEqual(user.email, "bek@go.com")
        self.assertEqual(response.url, reverse("users:profile"))