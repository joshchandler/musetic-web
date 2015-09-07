from django.dispatch import Signal

comment_created = Signal(providing_args=["comment", "request"])
