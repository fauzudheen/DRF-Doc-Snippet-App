from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics, permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.contrib.auth.models import User
from rest_framework import viewsets


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

'''
Note: It is not mandatory to name the variables as queryset and serializer_class, 
but that is the convention. The order of the two also does't matter.
When you define a subclass of RetrieveUpdateDestroyAPIView, DRF internally inspects 
the attributes of that class to identify which attribute corresponds to the queryset 
and which corresponds to the serializer class.

Eg:
        s = SnippetSerializer
        q = Snippet.objects.all()

This would also work

'''



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # This viewset automatically provides `list` and `retrieve` actions.
    queryset = User.objects.all()
    serializer_class = UserSerializer





