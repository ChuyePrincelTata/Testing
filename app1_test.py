import unittest
# from flask_testing import TestCase
from app1 import app, db, Post
from datetime import datetime

class FlaskBlogTests(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        test_post = Post(
            title='Test Post',
            content='This is a test post content',
            date_posted=datetime.utcnow()
        )
        db.session.add(test_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        """Test if home page loads correctly and displays posts"""
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('home.html')
        self.assertIn(b'Test Post', response.data)

    def test_about_page(self):
        """Test if about page loads correctly"""
        response = self.client.get('/about')
        self.assert200(response)
        self.assert_template_used('about.html')

    def test_create_post_page_get(self):
        """Test if create post page loads correctly"""
        response = self.client.get('/post/new')
        self.assert200(response)
        self.assert_template_used('create_post.html')

    def test_create_post_submission(self):
        """Test successful post creation"""
        response = self.client.post('/post/new', data={
            'title': 'New Test Post',
            'content': 'New test content'
        }, follow_redirects=True)
        
        self.assert200(response)
        self.assertIn(b'Your post has been created!', response.data)
        self.assertIn(b'New Test Post', response.data)

    def test_empty_post_submission(self):
        """Test submission with empty fields"""
        initial_count = Post.query.count()
        
        # Test empty title
        response = self.client.post('/post/new', data={
            'title': '',
            'content': 'Test content'
        }, follow_redirects=True)
        self.assertIn(b'Title and content are required!', response.data)
        
        # Test empty content
        response = self.client.post('/post/new', data={
            'title': 'Test Title',
            'content': ''
        }, follow_redirects=True)
        self.assertIn(b'Title and content are required!', response.data)
        
        # Verify no new posts were created
        final_count = Post.query.count()
        self.assertEqual(initial_count, final_count)

    def test_long_title_submission(self):
        """Test submission with title exceeding maximum length"""
        initial_count = Post.query.count()
        long_title = 'A' * 101
        
        response = self.client.post('/post/new', data={
            'title': long_title,
            'content': 'Test content'
        }, follow_redirects=True)
        
        self.assertIn(b'Title must be less than 100 characters!', response.data)
        final_count = Post.query.count()
        self.assertEqual(initial_count, final_count)

    def test_post_model(self):
        """Test Post model operations"""
        new_post = Post(title='DB Test', content='Testing database operations')
        db.session.add(new_post)
        db.session.commit()
        
        post = Post.query.filter_by(title='DB Test').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'Testing database operations')

    def test_flash_messages(self):
        """Test if flash messages are working"""
        response = self.client.post('/post/new', data={
            'title': 'Flash Test',
            'content': 'Testing flash messages'
        }, follow_redirects=True)
        
        self.assertIn(b'Your post has been created!', response.data)

if __name__ == '__main__':
    unittest.main()



    