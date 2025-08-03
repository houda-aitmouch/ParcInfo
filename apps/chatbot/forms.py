from django import forms

class ChatForm(forms.Form):
    """Formulaire pour l'interface de chat"""
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Posez votre question sur le système ParcInfo...',
            'id': 'chat-message'
        }),
        label='Votre message',
        max_length=1000
    ) 