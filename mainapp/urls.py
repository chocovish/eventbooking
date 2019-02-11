from django.urls import path,include
from rest_framework import routers
from rest_framework.authtoken import views as authviews
from . import views

router = routers.DefaultRouter()
router.register("tickets", views.TicketView) 
router.register("users", views.UserView) 
router.register("events", views.EventView) 
#router.register("eventsfilter", views.EventFilter) 

customs = [
    path('authuser/', authviews.obtain_auth_token),
    path('logout/', views.Logout.as_view()),
    path('changepass/<pk>/', views.ChangePasswordView.as_view()),
    path('eventsfilter/', views.EventFilter.as_view()),
    path('userevents/<pk>/', views.EventsBookedByUser.as_view()),
]
urlpatterns = router.urls + customs
