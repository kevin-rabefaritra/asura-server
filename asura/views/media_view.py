from django.forms import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from asura.auth import TokenAuthentication

from asura.services import post_services

class MediaCreate(APIView):
    """
    Used to create media
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        """
        Creates a new Media object
        @param request. Contains:
            - media <array> list of media as base64
        @param uuid the Post uuid
        """
        data = request.data
        try:
            if 'media' not in data:
                # if media is not defined
                return Response(status=status.HTTP_400_BAD_REQUEST)

            post = post_services.find_by_uuid(uuid)
            if not post:
                # Post does not exist
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            # Check that the authenticated User is the owner of the Post
            if post.user.uuid != request.user.uuid:
                # we can return a status 401 but this might be confused with the
                # user token being invalid or expired
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            post_services.add_media(data['media'], post.uuid)

            return Response(status=status.HTTP_201_CREATED)
        
        except ValidationError:
            # UUID not valid
            return Response(status=status.HTTP_404_NOT_FOUND)