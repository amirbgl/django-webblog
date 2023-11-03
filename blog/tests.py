from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from.models import Post

"""
    farghe (setUpTestData)va(setUp) toie ine ke setup baray har test yek bar dige object
    ra misazad vali setuptest data yek bar misazad va zakhire mi konad va har seri estefade
    mikonad va ravesh 2 be classmethod niaz darad
"""

class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user1')
        cls.post1 = Post.objects.create(
            title='Post1',
            text='this is descriotion os Post1',
            status=Post.STATUS_CHOISES[0][0],#published
            author=user,
        )
        cls.post2 = Post.objects.create(
            title="Post2",
            text="lorem post2",
            status=Post.STATUS_CHOISES[1][0],#draft
            author=user,
        )

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post) , post.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'post1')


    def test_post_list(self):
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_by_name(self):
        response=self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, 'Post1')

    def test_post_detail(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_by_name(self):
        response=self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)


    def test_post_detail_on_blog_detail_page(self):
        response=self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_status_404_if_post_id_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_in_posts(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'),{
            "title":"Some Title",
            "text": "Some text",
            'status':'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Some Title')
        self.assertEqual(Post.objects.last().text, 'Some text')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args = [self.post2.id]),{
            "title": 'Some Title updated',
            'text': 'Some text updated',
            'status':'pub',
            'author': self.post2.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Some Title updated')
        self.assertEqual(Post.objects.last().text, 'Some text updated')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args = [self.post2.id]))
        self.assertEqual(response.status_code, 302)
