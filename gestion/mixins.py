from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin que permite el acceso solo a usuarios autenticados con rol de 'administrador'.
    """

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.rol == "administrador"
        )
