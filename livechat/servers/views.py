from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from .models import Server, Category
from .serializer import ServerSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .schema import server_list_docs
# Create your views here.

class CategoryListViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self,request):
        serializer = CategorySerializer(self.queryset,many=True)
        return Response(serializer.data)


class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()

    @server_list_docs
    def list(self,request):
        """
        Retrieve a filtered list of servers based on query parameters.

        This method handles various query parameters to filter and annotate a queryset of servers. 
        The following query parameters are supported:
        
        - `category`: Filters servers by category name.
        - `qty`: Limits the number of servers returned.
        - `by_user`: Filters servers based on the authenticated user if set to "true".
        - `with_num_member`: Annotates the servers with the number of members if set to "true".
        - `by_serverid`: Filters servers by server ID.

        If `by_user` or `by_serverid` are set, the user must be authenticated. Raises an `AuthenticationFailed`
        exception if the user is not authenticated when required.

        Args:
            request (Request): The incoming HTTP request containing query parameters.

        Returns:
            Response: A serialized list of servers, potentially filtered and annotated based on the query parameters.

        Raises:
            AuthenticationFailed: If `by_user` or `by_serverid` are provided and the user is not authenticated.
            ValidationError: If an invalid or non-existent server ID is provided via `by_serverid`.
        """
        
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        with_num_member = request.query_params.get("with_num_member") == "true"
        by_serverid = request.query_params.get("by_serverid")

        # if by_user or by_serverid and not request.user.is_authenticated:
        #     raise AuthenticationFailed()
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()

        if with_num_member:
            self.queryset = self.queryset.annotate(num_member=Count("member"))

        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id =by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"server with server Id {by_serverid} Not Found")
            except ValueError: 
                raise ValidationError(detail=f"server with server Id {by_serverid} Not Found")
            
        if qty :
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(self.queryset, many=True,context={"num_member":with_num_member})
        return Response(serializer.data)