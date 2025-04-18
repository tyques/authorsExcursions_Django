# Generated by Django 5.1.6 on 2025-04-18 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('password', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('excID', models.AutoField(primary_key=True, serialize=False)),
                ('excName', models.CharField(max_length=200)),
                ('excCountry', models.CharField(max_length=100)),
                ('excCity', models.CharField(max_length=100)),
                ('excDate', models.DateTimeField()),
                ('peopleNumberCurrent', models.IntegerField(default=0)),
                ('childPresence', models.BooleanField(default=False)),
                ('ageRestrict', models.IntegerField(default=0)),
                ('pathDiff', models.CharField(blank=True, max_length=50)),
                ('excDesc', models.TextField()),
                ('excPrice', models.FloatField()),
                ('excScore', models.FloatField(default=0.0)),
                ('excStatus', models.SmallIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Tour',
                'verbose_name_plural': 'Tours',
            },
        ),
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authorsExcursions.user')),
            ],
            options={
                'verbose_name': 'Registered User',
                'verbose_name_plural': 'Registered Users',
            },
            bases=('authorsExcursions.user',),
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tours', models.ManyToManyField(related_name='catalogs', to='authorsExcursions.tour')),
            ],
            options={
                'verbose_name': 'Catalog',
                'verbose_name_plural': 'Catalogs',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='authorsExcursions.cart')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorsExcursions.tour')),
            ],
            options={
                'unique_together': {('cart', 'tour')},
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(through='authorsExcursions.CartItem', to='authorsExcursions.tour'),
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('registereduser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authorsExcursions.registereduser')),
            ],
            options={
                'verbose_name': 'Administrator',
                'verbose_name_plural': 'Administrators',
            },
            bases=('authorsExcursions.registereduser',),
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('registereduser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authorsExcursions.registereduser')),
            ],
            options={
                'verbose_name': 'Guide',
                'verbose_name_plural': 'Guides',
            },
            bases=('authorsExcursions.registereduser',),
        ),
        migrations.AddField(
            model_name='tour',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='visited_tours', to='authorsExcursions.registereduser'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderId', models.AutoField(primary_key=True, serialize=False)),
                ('cost', models.FloatField()),
                ('promocode', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('paymentMethod', models.CharField(blank=True, choices=[('CC', 'Credit Card'), ('PP', 'PayPal'), ('BT', 'Bank Transfer')], max_length=2)),
                ('tours', models.ManyToManyField(to='authorsExcursions.tour')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorsExcursions.registereduser')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.FloatField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorsExcursions.tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorsExcursions.registereduser')),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedbacks',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authorsExcursions.registereduser'),
        ),
        migrations.AddField(
            model_name='tour',
            name='guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tours', to='authorsExcursions.guide'),
        ),
    ]
