from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class   HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Sport', description='Description1', isbn='111111')
        user=CustomUser.objects.create(
        username="xurshid", first_name="xurshid", last_name="olimov", email="xurshidolimov017@gmail.com"
        )

        user.set_password("turkiston")
        user.save()

        review1=BookReview.objects.create(book=book, user=user, stars_given=3, comment="Very good")
        review2=BookReview.objects.create(book=book, user=user, stars_given=4, comment="Very nice")
        review3=BookReview.objects.create(book=book, user=user, stars_given=5, comment="Very ok")

        response=self.client.get(reverse("home_page")+"?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)