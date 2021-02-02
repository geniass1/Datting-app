from .models import NewUser
from django.forms import ModelForm, PasswordInput


class CreateUserForm(ModelForm):
    class Meta:
        model = NewUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': PasswordInput()
        }

    def save(self):
        self.instance.set_password(self.instance.password)
        super().save()
