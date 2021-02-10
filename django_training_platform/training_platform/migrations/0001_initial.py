# Generated by Django 3.1.4 on 2021-01-28 08:25

from django.db import migrations, models
import django.db.models.deletion
import training_platform.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(training_platform.models.CourseScopeModelInterface, models.Model),
        ),
        migrations.CreateModel(
            name='CompletedTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(training_platform.models.CourseScopeModelInterface, models.Model),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(training_platform.models.CourseScopeModelInterface, models.Model),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(training_platform.models.CourseScopeModelInterface, models.Model),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('content', models.TextField(blank=True)),
                ('file', models.FileField(null=True, upload_to='')),
            ],
            options={
                'abstract': False,
            },
            bases=(training_platform.models.CourseScopeModelInterface, models.Model),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='training_platform.lesson')),
            ],
            options={
                'abstract': False,
            },
            bases=(training_platform.models.CourseScopeModelInterface, models.Model),
        ),
    ]
