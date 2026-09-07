from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


ROLE_REQUEST_PERMISSIONS = [
    ("ROLE_REQUEST_VIEW", "View Role Requests"),
    ("ROLE_REQUEST_APPROVE", "Approve Role Requests"),
    ("ROLE_REQUEST_REJECT", "Reject Role Requests"),
]


def seed_role_request_permissions(apps, schema_editor):
    Permission = apps.get_model("ncrb_auth", "Permission")
    Role = apps.get_model("ncrb_auth", "Role")
    RolePermission = apps.get_model("ncrb_auth", "RolePermission")

    super_admin = Role.objects.filter(code="SUPER_ADMIN").first()
    if not super_admin:
        return

    for code, name in ROLE_REQUEST_PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(
            code=code,
            defaults={"name": name, "is_active": True},
        )
        RolePermission.objects.get_or_create(
            role=super_admin,
            permission=permission,
        )


def unseed_role_request_permissions(apps, schema_editor):
    Permission = apps.get_model("ncrb_auth", "Permission")
    RolePermission = apps.get_model("ncrb_auth", "RolePermission")
    codes = [code for code, _ in ROLE_REQUEST_PERMISSIONS]
    RolePermission.objects.filter(permission__code__in=codes).delete()
    Permission.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
    ("ncrb_auth", "0004_permission_rolepermission"),
]

    operations = [
        migrations.CreateModel(
            name="RoleRequest",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")], default="PENDING", max_length=20)),
                ("requested_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True)),
                ("requested_role", models.ForeignKey(db_column="requested_role_id", on_delete=django.db.models.deletion.RESTRICT, related_name="role_requests", to="ncrb_auth.role")),
                ("reviewed_by", models.ForeignKey(blank=True, db_column="reviewed_by_id", null=True, on_delete=django.db.models.deletion.RESTRICT, related_name="reviewed_role_requests", to="ncrb_auth.user")),
                ("user", models.ForeignKey(db_column="user_id", on_delete=django.db.models.deletion.CASCADE, related_name="role_requests", to="ncrb_auth.user")),
            ],
            options={
                "db_table": "role_requests",
                "ordering": ["-requested_at"],
                "indexes": [models.Index(fields=["status", "requested_at"], name="role_reques_status_64ce85_idx")],
            },
        ),
        migrations.RunPython(seed_role_request_permissions, unseed_role_request_permissions),
    ]
