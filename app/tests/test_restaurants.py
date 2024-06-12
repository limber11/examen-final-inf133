# tests/test_restaurants.py
import unittest
from app import app, db
from app.models import Restaurant

class RestaurantTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.headers = {'Content-Type': 'application/json'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_restaurant(self):
        response = self.app.post('/restaurants', json={
            'name': 'Test Restaurant',
            'address': '123 Test St',
            'city': 'Test City',
            'phone': '1234567890',
            'description': 'A test restaurant',
            'rating': 4.5
        }, headers=self.headers)
        self.assertEqual(response.status_code, 201)

    # Más pruebas aquí...

if __name__ == '__main__':
    unittest.main()
