from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import User


class UserCreationForm(forms.ModelForm):  # type: ignore
    """Form for user registration in admin panel"""

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:  # pylint: disable=missing-class-docstring
        model = User
        fields = (
            "email",
            "username",
            "password",
            "is_staff",
            "is_superuser",
        )

    def clean_password2(self) -> str:
        """Check that the two password entries match"""
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        assert isinstance(password2, str)
        return password2

    def save(self, commit: bool = True) -> User:
        """Save the provided password in hashed format"""
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):  # type: ignore
    """Form for change password"""

    password = ReadOnlyPasswordHashField()

    class Meta:  # pylint: disable=missing-class-docstring
        model = User
        fields = ("email", "username", "password", "is_active", "is_superuser")

    def clean_password(self) -> str:
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        ret = self.initial["password"]
        assert isinstance(ret, str)
        return ret
