from django.forms import ModelForm
from users_app.models import Users


class UserCreationForm(ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user