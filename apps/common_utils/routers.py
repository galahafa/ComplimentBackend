from rest_framework.routers import DefaultRouter


class CustomDefaultRouter(DefaultRouter):

    def __init__(self, trailing_slash=True):
        super().__init__()
        self.trailing_slash = '/?' if trailing_slash else ''
