# Generated by Django 3.0.7 on 2020-07-11 11:28

from django.db import migrations, models
import django.db.models.deletion


def fwd_restaurants(apps, schema_editor):
    Course = apps.get_model('restaurants', 'Course')
    for course in Course.objects.all():
        course.restaurant = course.restaurant_set.first()
        course.save()

def bkwd_restaurants(apps, schema_editor):
    Course = apps.get_model('restaurants', 'Course')
    for course in Course.objects.all():
        course.restaurant_set.set([course.restaurant])

class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20200709_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.Restaurant'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='menu',
            field=models.ManyToManyField(blank=True, related_name='restaurant_set', to='restaurants.Course'),
        ),
        migrations.RunPython(fwd_restaurants, bkwd_restaurants),
    ]
