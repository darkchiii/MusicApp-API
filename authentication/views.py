from rest_framework.authtoken.models import Token
from rest_framework.response import Response #generate json responses
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import UserSerializer 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status 
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
# class UserLoginView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [AllowAny]
#     # @api_view(['POST']) # jak to dodaje to token sie nie zwraca
#     # @permission_classes((permissions.AllowAny))
#     def post(self, request):
#         user = authenticate(username=request.data["username"], password=request.data["password"])
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key,
#                             # 'user_id': user.pk,
#                             })
#         else:
#             return Response({'error': 'Invalid Credentials'}, status=401)
        
@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    # print(request.data["username"]) #JAK SIE TO WYKONAĆ
    if not user.check_password(request.data["password"]):
        return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)