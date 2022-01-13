# Generated by Django 3.1.14 on 2022-01-13 19:36
import sys

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import nautobot.core.fields
import taggit.managers
import uuid


def cache_circuit_terminations(apps, schema_editor):
    Circuit = apps.get_model("circuits", "Circuit")
    CircuitTermination = apps.get_model("circuits", "CircuitTermination")

    if "test" not in sys.argv:
        print("\n    Caching circuit terminations...", flush=True)

    a_terminations = {ct.circuit_id: ct.pk for ct in CircuitTermination.objects.filter(term_side="A")}
    z_terminations = {ct.circuit_id: ct.pk for ct in CircuitTermination.objects.filter(term_side="Z")}
    for circuit in Circuit.objects.all():
        Circuit.objects.filter(pk=circuit.pk).update(
            termination_a_id=a_terminations.get(circuit.pk),
            termination_z_id=z_terminations.get(circuit.pk),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("circuits", "0003_auto_slug"),
        ("dcim", "0007_device_secrets_group"),
        ("extras", "0016_secret"),
    ]

    operations = [
        migrations.AddField(
            model_name="circuit",
            name="termination_a",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="circuits.circuittermination",
            ),
        ),
        migrations.AddField(
            model_name="circuit",
            name="termination_z",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="circuits.circuittermination",
            ),
        ),
        migrations.AlterField(
            model_name="circuittermination",
            name="site",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="circuit_terminations",
                to="dcim.site",
            ),
        ),
        migrations.CreateModel(
            name="ProviderNetwork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="provider_networks",
                        to="circuits.provider",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="extras.TaggedItem",
                        to="extras.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "ordering": ("provider", "name"),
            },
        ),
        migrations.AddField(
            model_name="circuittermination",
            name="provider_network",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="circuit_terminations",
                to="circuits.providernetwork",
            ),
        ),
        migrations.AddConstraint(
            model_name="providernetwork",
            constraint=models.UniqueConstraint(
                fields=("provider", "name"), name="circuits_providernetwork_provider_name"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="providernetwork",
            unique_together={("provider", "name")},
        ),
        migrations.RunPython(
            code=cache_circuit_terminations,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
        migrations.AddField(
            model_name="providernetwork",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
        ),
    ]
