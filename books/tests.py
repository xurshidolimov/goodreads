from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from books.models import Book
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_books(self):
        response=self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")


    def test_book_list(self):
        book1=Book.objects.create(title='Book1', description='Description1', isbn='111111')
        book2=Book.objects.create(title='Book2', description='Description2', isbn='222222')
        book3=Book.objects.create(title='Book3', description='Description3', isbn='333333')

        response = self.client.get(reverse("books:list")+"?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        self.assertNotContains(response, book3.title)

        response=self.client.get(reverse("books:list")+"?page=2&page_size=2")
        self.assertContains(response, book3.title)


    def test_detail_page(self):
        book=Book.objects.create(title='Book1', description='Description1', isbn='111111')

        response=self.client.get(reverse("books:detail", kwargs={"id":book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title='Sport', description='Description1', isbn='111111')
        book2 = Book.objects.create(title='News', description='Description2', isbn='222222')
        book3 = Book.objects.create(title='Global', description='Description3', isbn='333333')

        response=self.client.get(reverse("books:list")+"?q=sport")

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)




        response=self.client.get(reverse("books:list")+"?q=news")

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)




        response=self.client.get(reverse("books:list")+"?q=global")

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book=Book.objects.create(title='Book1', description='Description1', isbn='111111')

        user=CustomUser.objects.create(
            username="xurshid", first_name="xurshid", last_name="olimov", email="xurshidolimov017@gmail.com"
        )

        user.set_password("turkiston")
        user.save()

        self.client.login(username="xurshid", password="turkiston")

        self.client.post(reverse("books:reviews", kwargs={"id":book.id}), data={
            "stars_given":3,
            "comment":"Nice book"
        })

        book_reviews=book.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)


    #  bajarib ko'r mustaqil
    # def test_author(self):
    #     book = Book.objects.create(title='Book1', description='Description1', isbn='111111')
    #     user=CustomUser.objects.create(
    #         username="xurshid", first_name="xurshid", last_name="olimov", email="xurshidolimov017@gmail.com"
    #     )
    #
    #     user.set_password("turkiston")
    #     user.save()

