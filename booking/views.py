from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

template = PromptTemplate(
            input_variables=["user_input"],
            template="You are a helpful assistant. Answer the following:\n{user_input}"
        )

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo",  # or "gpt-4" if you have access
    temperature=0.7
)

chain = LLMChain(llm=llm, prompt=template)

class LangChainViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['post'], url_path='get_room_description')
    def get_room_description(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "No prompt provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            answer = chain.run(user_input=prompt)
            return Response(answer, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_200_OK)