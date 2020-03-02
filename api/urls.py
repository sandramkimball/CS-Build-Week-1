from django.urls import include, path
from django.conf.urls import url

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('api/', include(router.urls)),
    # path('graphql/', GraphQLView.as_view(graphiql=True))
]
