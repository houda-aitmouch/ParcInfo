# Generated manually for chatbot app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_alter_customuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message utilisateur')),
                ('response', models.TextField(verbose_name='Réponse du chatbot')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Date et heure')),
                ('session_id', models.CharField(blank=True, max_length=100, verbose_name='ID de session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to='users.customuser')),
            ],
            options={
                'verbose_name': 'Message de chat',
                'verbose_name_plural': 'Messages de chat',
                'ordering': ['-timestamp'],
            },
        ),
    ]