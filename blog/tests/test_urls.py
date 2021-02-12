from django.test import TestCase
from django.urls import reverse, resolve
from ..views import Index, Detail, CreateView, Update, Delete
from blog.models import Category, Post, Tag
from django.test import TestCase, Client
from registration.models import User 
from django.contrib.auth import get_user_model

User = get_user_model()
                    
                    
class TestUrls(TestCase):
    
    
         #トップページ/8000に移行するかテスト
         #blog/post_list.htmlを表示するかテスト
    def test_index_url(self):
        self.client = Client()
        user = User.objects.create_user(
            email = 'hayato.nomura@icloud.com',
            username = 'admin',
            password = 'adgjm135')
        self.client.force_login(user)
        self.assertEqual(user.password, 'adgjm135')
       
        
         #/detail/<pk>/に移行するかテスト
         #blog/post_detail.htmlを表示するかテスト
    def test_detail_url(self):
        category = Category(name='テストカテゴリー')
        category.save()
        tag = Tag(name='テストタグ')
        tag.save()
        post = Post(category=category,title='test_title',
                    body='test_body', published=1)
        post.save()
        
        url = reverse('blog:detail', kwargs={'pk': post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        template = 'blog/post_detail.html'
        self.assertTemplateUsed(template)
        
        
         #/create/に移行するかテスト
         #blog/post_form.htmlを表示するかテスト
    def test_create_url(self):
        self.client = Client()
        user = User.objects.create_user(
            username = 'nomura',
            password = 'adgjm135')
        self.client.force_login(user=user)
        url = reverse('blog:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        template = 'blog:post_form.html'
        self.assertTemplateUsed(template)
        
        
         #/update/<pk>/に移行するかテスト
         #blog/post_form.htmlを表示するかテスト
    def test_update_url(self):
        category = Category(name='テストカテゴリー')
        category.save()
        tag = Tag(name='テストタグ')
        tag.save()
        post = Post(category=category,title='test_title',
                    body='test_body', published=1)
        post.save()
        
        url = reverse('blog:update', kwargs={'pk': post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        template = 'blog:post_form.html'
        self.assertTemplateUsed(template)
        
        
         #/delete/<pk>/に移行するかテスト
         #blog/post_comfirm_delete.htmlを表示するかテスト
    def test_delete_url(self):
        category = Category(name='テストカテゴリー')
        category.save()
        tag = Tag(name='テストタグ')
        tag.save()
        post = Post(category=category,title='test_title',
                    body='test_body', published=1)
        post.save()
        
        url = reverse('blog:delete', kwargs={'pk': post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        template = 'blog/post_comfirm_delete.html'
        self.assertTemplateUsed(template)
        
        
     
        
        