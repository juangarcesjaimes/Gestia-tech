from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El usuario debe tener una dirección de correo electrónico.'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('El superusuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('El superusuario debe tener is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Correo Electrónico'), unique=True)
    username = models.CharField(_('Nombre de Usuario'), max_length=150, unique=True)
    first_name = models.CharField(_('Nombre'), max_length=30, blank=True)
    last_name = models.CharField(_('Apellido'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('Fecha de Registro'), default=timezone.now)
    is_active = models.BooleanField(_('Activo'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=False)
    profile_image = models.ImageField(_('Imagen de Perfil'), upload_to='profile_images/', blank=True, null=True)
    roles = models.ManyToManyField('Role', verbose_name=_('Roles'), blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return self.email

    def clean(self):
        if not self.email:
            raise ValidationError(_('El campo de correo electrónico no puede estar vacío.'))

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(_('Biografía'), blank=True, null=True)
    birth_date = models.DateField(_('Fecha de Nacimiento'), blank=True, null=True)
    location = models.CharField(_('Ubicación'), max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

# Role Model
class Role(models.Model):
    name = models.CharField(_('Nombre del Rol'), max_length=255)
    permissions = models.ManyToManyField('Permission', verbose_name=_('Permisos'), blank=True)

    class Meta:
        verbose_name = _('Rol')
        verbose_name_plural = _('Roles')

    def __str__(self):
        return self.name

# Permission Model
class Permission(models.Model):
    name = models.CharField(_('Nombre del Permiso'), max_length=255)

    class Meta:
        verbose_name = _('Permiso')
        verbose_name_plural = _('Permisos')

    def __str__(self):
        return self.name

# User Activity Log
class UserActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(_('Acción'), max_length=255)
    timestamp = models.DateTimeField(_('Fecha y Hora'), auto_now_add=True)

    class Meta:
        verbose_name = _('Registro de Actividad del Usuario')
        verbose_name_plural = _('Registros de Actividades de Usuarios')

    def __str__(self):
        return f'{self.user.email} - {self.action}'

# Audit Log for Tracking User Changes
class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    change = models.TextField(_('Cambio realizado'))
    timestamp = models.DateTimeField(_('Fecha y Hora'), auto_now_add=True)

    class Meta:
        verbose_name = _('Registro de Auditoría')
        verbose_name_plural = _('Registros de Auditoría')

    def __str__(self):
        return f'Auditoría de {self.user.email} el {self.timestamp}'
