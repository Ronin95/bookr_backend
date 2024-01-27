from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Agent
import json
from .serializers import AgentSerializer
from .utils import generateAgentAnswer
from django.utils.dateparse import parse_datetime

@api_view(['GET', 'POST'])
def agent_view(request):
    if request.method == 'GET':
        agents = Agent.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        user_input = request.data.get('user_messages', [])  # Assuming this sends a list of messages
        ai_response = generateAgentAnswer(user_input[0] if user_input else "")  # Getting the first message
        timestamp_str = request.data.get('timestamp', None)
        timestamp = parse_datetime(timestamp_str) if timestamp_str else None

        new_agent = Agent.objects.create(
            user_messages=user_input,  # Storing the whole list of user messages
            agent_messages=ai_response,  # Storing the AI response directly
            timestamp = timestamp
        )

        serializer = AgentSerializer(new_agent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

