# Generated by Django 3.1.4 on 2021-02-09 12:42

from django.db import migrations, models
import django.db.models.deletion
# from django.db.
# from django.apps import apps
from training_platform.models import Comment, Grade, CompletedTask, Task


def set_my_defaults(apps, schema_editor):
    app_config = apps.get_app_config('training_platform')
    models_to_change = ['Comment', 'Grade', 'CompletedTask', 'Task']
    models_to_change = [Comment, Grade, CompletedTask, Task]
    for model_to_change in models_to_change:
        # model = app_config.get_model(model_to_change)
        model = model_to_change
        for model_record in model.objects.all().iterator():
            model_record.course = model_record.get_associated_course
            model_record.save()
    # Series = AppConfig.get_model('Series')
    # for series in Series.objects.all().iterator():
    #     series.updated_as = datetime.now() + timedelta(days=series.some_other_field)
    #     series.save()


class Migration(migrations.Migration):

    dependencies = [
        ('training_platform', '0003_auto_20210209_1234'),
    ]

    operations = [
        migrations.RunPython(set_my_defaults, migrations.RunPython.noop),

        # migrations.AlterField(
        #     model_name='comment',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments',
        #                             to='training_platform.course'),
        # ),
        # migrations.AlterField(
        #     model_name='completedtask',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
        #                             related_name='completed_tasks', to='training_platform.course'),
        # ),
        # migrations.AlterField(
        #     model_name='grade',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades',
        #                             to='training_platform.course'),
        # ),
        # migrations.AlterField(
        #     model_name='task',
        #     name='course',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks',
        #                             to='training_platform.course'),
        # ),
    ]
