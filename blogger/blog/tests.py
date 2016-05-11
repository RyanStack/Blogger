import datetime

from django.utils import timezone
from django.test import TestCase, LiveServerTestCase, Client
from django_webtest import WebTest
from django.core.urlresolvers import reverse

from .models import Post
from .forms import PostForm

# Unit Tests
class PostTests(TestCase):

    def test_create_post(self):
        """
        Test that we can:
        1) Set the title
		2) Set the description
		3) Set the created_date
		4) Save object successfully 
		5) Retrieve object successfully
        """
        post = Post(title="Test post", description="Testing Post", created_date=timezone.now())
        post.save()
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        self.assertEquals(only_post.title, 'Test post')
        self.assertEquals(only_post.description, 'Testing Post')
        self.assertEquals(only_post.created_date.day, post.created_date.day)
        self.assertEquals(only_post.created_date.month, post.created_date.month)
        self.assertEquals(only_post.created_date.year, post.created_date.year)
        self.assertEquals(only_post.created_date.hour, post.created_date.hour)
        self.assertEquals(only_post.created_date.minute, post.created_date.minute)
        self.assertEquals(only_post.created_date.second, post.created_date.second)

# Acceptance Tests
class PostListViewTests(TestCase):
    def test_post_list_view_with_no_posts(self):
        """
        If no posts exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_post_list_view_with_new_post(self):
        """
        Newly created posts should be displayed on the post list view page.
        """
        create_post(title="Test Post", description="Testing Post", days=0)
        response = self.client.get(reverse('blog:list'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Test Post>']
        )

    def test_post_list_view_with_two_new_posts(self):
        """
        Two newly created posts should be displayed on post list view page.
        """
        create_post(title="Test Post 1", description="Testing Post 1", days=0)
        create_post(title="Test Post 2", description="Testing Post 2", days=0)
        response = self.client.get(reverse('blog:list'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Test Post 2>', '<Post: Test Post 1>']
        )

    def test_post_list_view_displays_most_recently_created_posts_first(self):
        """
        Most recently created posts(determined by created_date field) should be displayed first, 
        even if the post object was contextually created last.  
        """
        create_post(title="Test Post 1", description="Testing Post 1", days=0)
        create_post(title="Test Post 2", description="Testing Post 2", days=-10)
        create_post(title="Test Post 3", description="Testing Post 3", days=-5)
        response = self.client.get(reverse('blog:list'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Test Post 1>', '<Post: Test Post 3>', '<Post: Test Post 2>']
        )

class PostDetailsViewTests(TestCase):
    def test_post_details_view_with_non_existant_post_id(self):
        """
        Attempting to access the details view with a non-existant post_id should result in a 404 error.
        """
        random_post_id = 1
        response = self.client.get(reverse('blog:details', args=(random_post_id,)))
        self.assertEqual(response.status_code, 404)

    def test_post_details_view_with_a_new_post_id(self):
        """
        The details view of a new post should display the 
        title, description, and created_date.
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=0)
        response = self.client.get(reverse('blog:details', args=(post.id,)))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(post.title in response.content)
        self.assertTrue(post.description in response.content)
        self.assertTrue(str(post.created_date.year) in response.content)
        self.assertTrue(post.created_date.strftime('%b') in response.content)
        self.assertTrue(str(post.created_date.day) in response.content)
        # Still need to add time ex:1:01 a.m. 


class PostCreateViewTests(WebTest):
	# Improve this test so that I can reference the form class and isolate dependencies
    def test_post_create_view_get(self):
        """
        The post create view (method:GET) should display post form.
        """
        page = self.app.get(reverse('blog:create'))
        self.assertEqual(len(page.forms), 1)

    def test_post_create_view_post(self):
        """
        The post create view (method:POST) should create a new post 
        and redirect to the post list view. New post should also 
        be present in post list view.
        """
        response = self.client.post(reverse('blog:create'), {
            'title': 'Test Post 1',
            'description': 'Testing Post 1',
            'created_date': timezone.now()
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        self.assertTrue('Tivix Blogger' in response.content)
        self.assertTrue('Test Post 1' in response.content)

    # def test_post_form_success(self):
    #     """
    #     The post create view(post method) should create a new post 
    #     and redirect to the post list view. New post should also 
    #     be present in post list view.
    #     """
    #     page = self.app.get(reverse('blog:create'))
    #     page.form['title'] = 'Test Post 1'
    #     page.form['description'] = 'Testing Post 1'
    #     page.form.submit()
    #     self.assertRedirects(page, reverse('blog:list'))

    def test_form_error(self):
    	"""
        Error messages should be displayed when user inputs invalid data
        """
    	page = self.app.get(reverse('blog:create'))
    	page = page.form.submit()
    	self.assertContains(page, "This field is required.")
    
    # def test_form_error2(self):
    # 	"""
    #     Error messages should be displayed when user inputs invalid data
    #     """
    # 	page = self.app.get(reverse('blog:create'))
    # 	page.form['title'] = 'Toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo Looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong'
    # 	page.form['description'] = 'Testing Post 1'
    # 	page = page.form.submit()
    # 	self.assertContains(page, "This field is required.") 

class PostUpdateViewTests(WebTest):
    def test_post_update_view_get(self):
        """
        The post update view (method:GET) should display post update form. Title, 
        description and id should correspond to appropriate values.
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=0)
        page = self.app.get(reverse('blog:update', args=(post.id,)))
        self.assertEqual(len(page.forms), 1)
        self.assertEqual(page.form.action, '/blog/' + str(post.id) + '/update/')
        self.assertEqual(page.form['title'].value, 'Test Post 1')
        self.assertEqual(page.form['description'].value, 'Testing Post 1')

    def test_post_update_view_post(self):
        """
        The post update view (method:POST) should update a post and redirect to the 
        post list view. Updated title should be present in post list view.
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=0)
        response = self.client.post(reverse('blog:update', args=(post.id,)), {
            'title': 'Test Post 2',
            'description': 'Testing Post 2'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Test Post 2' in response.content) 
        
    def test_post_request_no_new_posts(self):
        """
        The post update view (method:POST) should only update a post, not create a 
        new post. 
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=0)
        response = self.client.post(reverse('blog:update', args=(post.id,)), {
            'title': 'Test Post 2',
            'description': 'Testing Post 2'
        }, follow=True)
        self.assertEquals(response.status_code, 200)
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_post_request_and_then_details_view(self):
        """
        The post update view (method:POST) should update a post, and updated info
        should be accurately reflected in the details view.  Created_date field 
        should remain the same (in the past).
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=-10)
        self.client.post(reverse('blog:update', args=(post.id,)), {
            'title': 'Test Post 2',
            'description': 'Testing Post 2'
        })
        response = self.client.get(reverse('blog:details', args=(post.id,)))
        self.assertTrue('Test Post 2' in response.content)
        self.assertTrue('Testing Post 2' in response.content)
        self.assertTrue(str(post.created_date.year) in response.content)
        self.assertTrue(post.created_date.strftime('%b') in response.content)
        self.assertTrue(str(post.created_date.day) in response.content)
        # Still need to add time ex:1:01 a.m. 

    def test_form_error(self):
    	"""
        Error messages should be displayed when user inputs invalid data.
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=0)
    	page = self.app.get(reverse('blog:update', args=(post.id,)))
    	page.form['title'] = ''
        page.form['description'] = ''
    	page = page.form.submit()
    	self.assertContains(page, "This field is required.")

class PostDeleteViewTests(WebTest):
    def test_delete_post_view_get(self):
        """
        If a user clicks on delete, they will be brought to a confirmation page with 
        correct post's information.
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=0)
        page = self.app.get(reverse('blog:delete', args=(post.id,)))
        self.assertEqual(len(page.forms), 1)
        self.assertEqual(page.form.action, '/blog/' + str(post.id) + '/delete/')
        self.assertContains(page, 'Test Post 1')

    def test_delete_post_view_post(self):
        """
        If a user confirms delete (method:POST), the post should be deleted, the
        user should be redirected to the post list view, and the most recently 
        deleted post should not be present.
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=0)
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        response = self.client.post(reverse('blog:delete', args=(post.id,)), {}, follow=True)
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(post.title in response.content)

    def test_associated_links_after_delete_post(self):
        """
        If a user confirms delete (method:POST), the user should no longer be able 
        to navigate to the post's respective detail, update, and delete views.  
        """
        post = create_post(title="Test Post 1", description="Testing Post 1", days=0)
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        self.client.post(reverse('blog:delete', args=(post.id,)), {}, follow=True)
        response1 = self.client.get(reverse('blog:details', args=(post.id,)))
        self.assertEqual(response1.status_code, 404)
        response2 = self.client.get(reverse('blog:update', args=(post.id,)))
        self.assertEqual(response2.status_code, 404)
        response3 = self.client.get(reverse('blog:delete', args=(post.id,)))
        self.assertEqual(response3.status_code, 404)
        

# Helper Functions
def create_post(title, description, days):
	"""
	Creates a post object. Allows manipulation of the current date/time.
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Post.objects.create(title=title, description=description, created_date=time)

        
