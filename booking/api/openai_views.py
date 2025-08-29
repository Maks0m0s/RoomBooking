from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from booking.services import openai_service

class OpenAIViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['post'], url_path='get_room_description')
    def get_room_description(self, request):
        prompt = request.data.get('prompt')
        if not prompt:
            return Response('Error : "prompt" argument is required.', status=status.HTTP_400_BAD_REQUEST)
        result = openai_service.get_openai_response(prompt)
        return Response(result, status=status.HTTP_200_OK)