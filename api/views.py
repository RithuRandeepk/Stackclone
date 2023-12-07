from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from api.serializer import UserSerializer,QuesionSerializer,AnswerSerializer
from api.models import Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import serializers

# Create your views here.
class UserView(viewsets.ViewSet):

    def create(self,request,*args,**kwargs):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(data=serializer.data)
        else:

            return Response(data=serializer.errors)

class QuestionsView(viewsets.ModelViewSet):

    serializer_class = QuesionSerializer
    queryset = Questions.objects.all()

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes =[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = QuesionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    # def list(self, request, *args, **kwargs):
    #     qs = Questions.objects.all().exclude(user=request.user)
    #     serializer = QuesionSerializer(qs,many=True)
    #     return Response(data=serializer.data)

    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)
        

# localhost:8000/questions/2/add_answer/
   
    @action(methods=["POST"],detail=True)
    def add_answer(self,request,*args,**kwargs):

        object = self.get_object()
        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid():
         serializer.save(user=request.user,question=object)
         return Response(data=serializer.data)

       
    
        else:
         return Response(data=serializer.errors)



class AnswerView(viewsets.ModelViewSet):

    serializer_class = AnswerSerializer
    queryset = Answers.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
        
        raise serializers.ValidationError("method not found")
    
    def list(self,request,*args,**kwargs):

        raise serializers.ValidationError("method not found")
    
    def destroy(self, request, *args, **kwargs):
        
        object = self.get_object()

        if request.user == object.user:

            object.delete()
            return Response(data="deleted")
        
        else:

            raise serializers.ValidationError("Permission denied for this user")
        
    @action(methods=["POST"],detail=True)
    
    def add_upvote(self,request,*args,**kwargs):

        object = self.get_object()
        user = request.user
        object.upvote.add(user)
        return Response(data='up voted')
    
        




