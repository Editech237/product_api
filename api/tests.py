from django.test import TestCase
from django.urls import reverse
from api.models import Order, User
from rest_framework import status



class UserOrderTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)
    


    def test_order_enpoind_retrieves_only_authenticated_users_orders(self):
        user = User.objects.get(username = 'user1')
        self.client.force_login(user)
        response = self.client.get(reverse('user-orders'))

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()

        # checking to make sure the logged in user id is the same with the user in the other
        # Also the all() method returns a boolean for a list of iterable booleans, so if onne is false, the resulting will be false
        self.assertTrue(all(order['user'] == user.id for order in orders))

    # if by mistake someone removes the IsAuthenticated permission in the views class,
    # we can write a smalltest on this
    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
