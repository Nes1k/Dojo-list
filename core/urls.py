from django.conf.urls import include, url, patterns
from rest_framework_nested import routers

from core.api import ListViewSet, ActionViewSet
from core.views import HomeView

# trailing_slash=False
router = routers.SimpleRouter()
router.register(r'list', ListViewSet, 'list')

domains_route = routers.NestedSimpleRouter(router, r'list', lookup='list')
domains_route.register(r'actions', ActionViewSet, 'actions')

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^', include(router.urls)),
    url(r'^', include(domains_route.urls))
)
