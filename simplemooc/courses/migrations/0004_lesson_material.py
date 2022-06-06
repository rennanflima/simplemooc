# Generated by Django 3.2.13 on 2022-06-06 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_announcement_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('description', models.TextField(blank=True, verbose_name='descrição')),
                ('number', models.IntegerField(blank=True, default=0, verbose_name='número (ordem)')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='data de liberação')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lessons', to='courses.course', verbose_name='curso')),
            ],
            options={
                'verbose_name': 'aula',
                'verbose_name_plural': 'aulas',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('embedded', models.TextField(blank=True, verbose_name='conteúdo incorporado')),
                ('file', models.FileField(blank=True, null=True, upload_to='lessons/materials', verbose_name='arquivo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='courses.lesson', verbose_name='aula')),
            ],
            options={
                'verbose_name': 'material',
                'verbose_name_plural': 'materiais',
            },
        ),
    ]
