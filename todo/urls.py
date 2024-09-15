from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views
from . views import UsersInfo, PriorityChoiceViewset, ProfileInfo

router= DefaultRouter()
router.register('list', views.TodoView)
router.register('users', UsersInfo)
router.register('priority_choice',PriorityChoiceViewset)
router.register('profiles',ProfileInfo)


urlpatterns = [
    # path('todosika/', views.ToapiView.as_view()),
    path('', include(router.urls)),
    path('register/', views.UserRegistrationApiView.as_view() , name='register'),
    path('login/', views.UserLoginApiView.as_view() , name='login'),
    path('logout/', views.UserLogoutView.as_view() , name='logout'),
    path('active/<uid64>/<token>/', views.activate, name='activate'),

]