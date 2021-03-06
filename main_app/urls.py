from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('travels/', views.Travel_List.as_view(), name='travel_list'),
    path('travels/new', views.travel_create, name='travel_create'),
    path('travels/<int:pk>', views.travel_detail, name='travel_detail'),
    path('travels/<int:pk>/update', views.Travel_Update.as_view(), name='travel_update'),
    path('travels/<int:pk>/delete', views.Travel_Delete.as_view(), name='travel_delete'),

    path('travels/<int:pk>/itineraries/new', views.Itinerary_Create.as_view(), name='itinerary_create'),
    path('travels/<int:pk>/itineraries/<int:itinerary_id>/update', views.itinerary_update, name='itinerary_update'),
    path('travels/<int:pk>/itineraries/<int:itinerary_id>/delete', views.itinerary_delete, name='itinerary_delete'),

    path('travels/<int:pk>/checklists', views.checklist_list, name='checklist_list'),
    path('travels/<int:pk>/checklists/<int:item_id>/completed', views.is_completed, name="is_completed"),
    path('travels/<int:pk>/checklists/<int:item_id>/notdone', views.is_not_done, name="is_not_done"),
    path('travels/<int:pk>/checklists/<int:item_id>/update', views.checklist_update, name="checklist_update"),
    path('travels/<int:pk>/checklists/<int:item_id>/delete', views.checklist_delete, name="checklist_delete"),

    path('travels/<int:pk>/comments/<int:comment_id>/update', views.comment_update, name='comment_update'),
    path('travels/<int:pk>/comments/<int:comment_id>/delete', views.comment_delete, name='comment_delete'),

    path('destinations/', views.Destination_List.as_view(), name='destination_list'),
    path('destinations/new', views.Destination_Create.as_view(), name='destination_create'),
    path('destinations/<int:pk>', views.Destination_Detail.as_view(), name='destination_detail'),
    path('destinations/<int:pk>/update', views.Destination_Update.as_view(), name='destination_update'),
    path('destinations/<int:pk>/delete', views.Destination_Delete.as_view(), name='destination_delete'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),

    path('user/<username>', views.profile, name='profile'),
    path('user/<int:pk>/update', views.Profile_Update.as_view(), name='profile_update'),

    # path('users/', views.Users.as_view(), name='users')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)