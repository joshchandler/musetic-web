from django.test import TestCase
from musetic.user.forms import InviteForm, AcceptInvitationForm
from musetic.user.models import User

from django_dynamic_fixture import G

class InviteFormTest(TestCase):
    
    def setUp(self):
        self.data = {'invitee': 'invitee@example.com'}
    
    def test_init(self):
        InviteForm(self.data)
        
    def test_form_validation(self):
        invite_form = InviteForm(self.data)
        self.assertTrue(invite_form.is_valid())
    
    def test_form_validation_fails_for_existing_user(self):
        user = G(User, email='invitedalready@example.com')
        invite_form = InviteForm({'invitee': 'invitedalready@example.com'})
        self.assertFalse(invite_form.is_valid())
        
        
class AcceptInvitationFormTest(TestCase):
    
    def setUp(self):
        self.data = {'username': 'invitee',
                     'password1': 'password',
                     'password2': 'password'}
    
    def test_init(self):
        AcceptInvitationForm(self.data)
     
    def test_form_validation(self):
        invite_accepted_form = AcceptInvitationForm(self.data)
        self.assertTrue(invite_accepted_form.is_valid())

    def test_username_already_exists(self):
        user = G(User, username='invitee')
        form = AcceptInvitationForm(self.data)
        self.assertFalse(form.is_valid())
    
    def test_validation_fails_on_different_passwords(self):
        invitee = {'username': 'invitee', 'password1': 'password', 'password2': 'diffpassword'}
        form = AcceptInvitationForm(invitee)
        self.assertFalse(form.is_valid())
        
        
        
        
        
        
        