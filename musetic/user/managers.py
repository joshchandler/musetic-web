import hashlib
import random
import re

from django.db import models
from django.utils import six

from django.contrib.auth.models import User


SHA1_RE = re.compile('^[a-f0-9]{40}$')


class CreatorManager(models.Manager):
    """
    A custom manager for the `UserCreator` Model
    """
    def activate_creator(self, user, site, send_email=True, request=None):
        """
        Activate the Creator by changing `is_creator` field to True
        """
        creator = self.get(user=user)
        creator.is_creator = True
        creator.save()

        if send_email:
            creator.send_acceptance_email(site, request)

        return creator

    def create_inactive_creator(self, user, url, site, send_email=True, request=None):
        """
        Creates a new creator entry, and emails the information at join@musetic.com
        """
        creator = self.create(user=user, url=url, is_creator=False)

        if send_email:
            creator.send_creator_request_email(site, request)

        return creator


class InviteManager(models.Manager):
    def create_invitation(self, inviter, invitee, site, request=None):
        salt = hashlib.sha1(six.text_type(random.random()).encode('ascii')).hexdigest()[:5]
        salt = salt.encode('ascii')
        email = invitee
        if isinstance(email, six.text_type):
            email = email.encode('utf-8')
        activation_key = hashlib.sha1(salt+email).hexdigest()

        invitation = self.create(
            inviter=inviter,
            activation_key=activation_key,
            invitee=invitee,
            accepted=False
        )

        invitation.send_invitation_email(site, request)

        return invitation

    def accept_invitation(self, invite, username, email, password, site, send_email=True, request=None):
        """
        Create the new user once they have accepted the invite
        :param invite: The Invite object
        :param username: invitee's username
        :param email: invitee's email
        :param password: invitee's password
        :param send_email: Whether to send an email to the inviter or not
        :return: new_user
        """
        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if send_email:
            invite.send_invite_accepted_email(new_user, site, request)

        return new_user
