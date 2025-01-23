from django.db import models

# Create your models here.



class Registration_table(models.Model): 
    user_name=models.CharField(max_length=100,null=True,blank=True)
    phone_number=models.IntegerField(null=True,blank=True)
    password=models.CharField(max_length=8,null=True,blank=True)
    
   



class ChatHistory(models.Model):

    user_query = models.TextField()  # User's query
    chatbot_response = models.TextField()  # Chatbot's response
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the interaction

    def _str_(self):
        return f"Chat at {self.timestamp}"

class SumHistory(models.Model):
    file_name=models.CharField(max_length=50,null=True,blank=True)
    summerize=models.CharField(max_length=50,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
