from django.test import TestCase

from cs_profile.models import Profile
from cs_profile.serializers import ProfileSerializer


class ProfileSerializerTestCase(TestCase):
    @property
    def profile_dict(self) -> dict:
        return {
            'id': 1,
            'public_name': 'my name',
            'public_address': 'my_address',
            'avatar_url': 'https://www.myavatar.com',
            'is_verified': True,
            'is_deleted': False,
        }

    @property
    def input_json(self) -> dict:
        profile_dict = {
            'id': 1,
            'publicName': 'my name',
            'publicAddress': {'id': 1, 'description': 'my address', },
            'avatarUrl': 'https://www.myavatar.com',
            'isVerified': True,
            'isDeleted': False,
        }
        return profile_dict

    @property
    def output_json(self) -> dict:
        profile_dict = {
            'id': 1,
            'publicName': 'my name',
            'publicAddress': 'my_address',
            'avatarUrl': 'https://www.myavatar.com',
            'isVerified': True,
            'isDeleted': False,
        }
        return profile_dict

    def test_that_profile_can_be_serialized(self):
        profile_dict = self.profile_dict
        profile = Profile.objects.create(**profile_dict)

        serializer = ProfileSerializer(profile)
        self.assertDictEqual(self.output_json, serializer.data)

    def test_that_profile_can_be_deserialized_create(self):
        serializer = ProfileSerializer(data=self.input_json)
        if not serializer.is_valid(raise_exception=False):
            self.fail('Profile dict cannot be deserialized: {}'.format(serializer.errors))
        profile = serializer.save()

        expected_profile = Profile(**self.profile_dict)
        self.assertEqual(expected_profile, profile)

    def test_that_profile_can_be_deserialized_update(self):
        profile_dict = self.profile_dict
        profile = Profile.objects.create(**profile_dict)

        data = self.input_json
        data['publicAddress'] = {'id': 2, 'description': 'my new address'}
        serializer = ProfileSerializer(instance = profile, data=data)
        if not serializer.is_valid(raise_exception=False):
            self.fail('Profile dict cannot be deserialized: {}'.format(serializer.errors))
        profile = serializer.save()

        self.assertEqual('my new address', profile.public_address)
