from django.contrib.auth.mixins import UserPassesTestMixin


class ProjectAccessMixin(UserPassesTestMixin):

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        self.object = self.get_object()
        if self.object.is_private and self.request.user not in self.object.members.all:
            self.raise_exception = True
            return False
        return True
