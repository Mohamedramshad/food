from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra__fields):
        extra__fields.setdefault("is_staff", True)
        extra__fields.setdefault("is_superuser", True)
        extra__fields.setdefault("is_active", True)

        if extra__fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra__fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra__fields)