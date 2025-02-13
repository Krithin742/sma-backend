from django.shortcuts import render

from .serializers import *


from rest_framework.views import APIView


# Create your views here.

class login(APIView):

    def post(self, request):

        response_dict = {}


        # Get data from the request

        user_name = request.data.get("username")

        password = request.data.get("password")


        # Validate input

        if not username or not password:

            response_dict["message"] = "failed"

            return Response(response_dict, status=HTTP_400_BAD_REQUEST)


        # Fetch the user from LoginTable

        t_user = LoginTable.objects.filter(username=username).first()


        if not t_user:

            response_dict["message"] = "failed"

            return Response(response_dict, status=HTTP_401_UNAUTHORIZED)


        # Check password using check_password

        if not check_password(password, t_user.password):

            response_dict["message"] = "failed"

            return Response(response_dict, status=HTTP_401_UNAUTHORIZED)


        # Successful login response

        response_dict["message"] = "success"

        response_dict["login_id"] = t_user.id


        return Response(response_dict, status=HTTP_200_OK)
    

class user_registration(APIView):

    def post(self,request):

        serializer=Loginserializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(response_dict,status=status.HTTP_400_BAD_REQUEST)

import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response


# Initialize Google Gemini API
genai.configure(api_key="AIzaSyAEXUDBa8makEQ6FPGDH1FvDqvIZGTQifc")  # Replace with your Gemini API key


class chatbotapi(APIView):
    def post(self, request):
        # Get query from the user input
        user_query = request.data.get('query', '')
         # Extract budget from the request if provided, default to 1000 INR

        # Default response if no input
        response_data = {

            'chatbot_response': "",
            "chat_history": [],   # This will store the chatbot-like response
        }





        # Construct the prompt using the filtered data (ensure it's only from the models)
        print(user_query)
        prompt = (
            f"User Query: {user_query}. "

            f"Provide the response based on above data"
        )

        try:
            # Call Gemini API to generate the response
            gemini_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            gemini_chatbot_response = gemini_response.text.strip()
            print(user_query)
            ChatHistory.objects.create(
                user_query=user_query,
                chatbot_response=gemini_chatbot_response,
            )

            # Update response data with the chatbot response
            response_data['chatbot_response'] = gemini_chatbot_response
                        # Retrieve the chat history
            chat_history = ChatHistory.objects.order_by("-timestamp").values(
                "user_query", "chatbot_response", "timestamp"
            )
            response_data.update(
                {

                    "chatbot_response": gemini_chatbot_response,
                    "chat_history": list(chat_history),
                }
            )

            



            # Return the chatbot-like response with the itinerary data
            return Response(response_data, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)