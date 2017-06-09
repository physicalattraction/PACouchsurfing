from rest_framework import serializers

from cs_profile.models import Profile


class AddressField(serializers.Field):
    def to_representation(self, obj: str) -> str:
        """
        When outputting the address, we simply present the address itself
        """
        return obj

    def to_internal_value(self, data: dict) -> str:
        """
        When the address is received as input, we need to extract the address itself from the dictionary
        """
        assert isinstance(data, dict)
        return data.get('description', '')


class ProfileSerializer(serializers.ModelSerializer):
    publicName = serializers.CharField(source='public_name')
    publicAddress = AddressField(required=False, allow_null=True, source='public_address')
    avatarUrl = serializers.CharField(source='avatar_url')
    isVerified = serializers.BooleanField(source='is_verified')
    isDeleted = serializers.BooleanField(source='is_deleted')

    class Meta:
        model = Profile
        fields = ('id', 'publicName', 'publicAddress', 'avatarUrl', 'isVerified', 'isDeleted')
        # extra_kwargs = {'id': {'read_only': False, 'required': True}}
