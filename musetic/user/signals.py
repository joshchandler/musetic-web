from django.dispatch import Signal

creator_registered = Signal(providing_args=["creator", "request"])

creator_accepted = Signal(providing_args=["creator", "request"])

invitation_sent = Signal(providing_args=["invitation", "request"])

invitation_accepted = Signal(providing_args=["invitation", "request"])
