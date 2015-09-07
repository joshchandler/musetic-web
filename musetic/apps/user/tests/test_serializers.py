from musetic.tests.testcase import MuseticTestCase
from musetic.apps.user.serializers import UserSerializer, ProfileSerializer, CreatorSerializer
from musetic.apps.user.models import User, Profile, Creator


class UserSerializerTests(MuseticTestCase):

    def test_user_serialized_data(self):
        self.maxDiff = None
        u = User.objects.get(username='foo')
        data = UserSerializer(u).data

        self.assertEquals(u.username, data['username'])
        self.assertEquals(u.first_name, data['first_name'])
        self.assertEquals(u.email, data['email'])


class ProfileSerializerTests(MuseticTestCase):

    def test_profile_serialized_data(self):
        self.maxDiff = None
        p = Profile.objects.get(user__username='foo')
        data = ProfileSerializer(p).data

        self.assertEquals('', data['description'])
        self.assertEquals('foo', data['user']['username'])


class CreatorSerializerTests(MuseticTestCase):

    def test_creator_serialized_data(self):
        self.maxDiff = None
        c = Creator.objects.get(user__username='foo')
        data = CreatorSerializer(c).data

        self.assertEquals(True, data['is_creator'])
        self.assertEquals(c.user.username, data['user']['username'])
