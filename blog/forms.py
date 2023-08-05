from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
          "user_name": "Your Name",
          "user_email": "Your Email",
          "text": "Your Comment"
        }
        
        
class ContactMeForm(forms.Form):
    
     user_name = forms.CharField(max_length=120, label="Your Name")
     user_email =  forms.EmailField(label="Your Email")
     attachment = forms.ImageField(label="Your Image")
     text = forms.CharField(
       max_length=400, label="Your Message", widget=forms.Textarea)
