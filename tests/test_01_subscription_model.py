import pytest


class Test01SubsctiptionModel:

    @pytest.mark.django_db(transaction=True)
    def test_create_user(self, django_user_model):
        user = django_user_model.objects.create(username='test', email='test@test.fake', first_name='x', last_name='y')
        assert user.username == 'test'
