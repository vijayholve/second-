from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from accounts.views import create_profile

urlpatterns = [
path("",views.home,name="home"),
path("review-user/",views.review_user,name="review_user"),
path("about/",views.about,name="about"),
path("services/",views.services,name="services"),
path("contact/",views.conatct,name="contact"),
path("login-page/",views.login_page,name="login-page"),
path("logout-page/",views.logout_page,name="logout-page"),    
path("register/",views.register,name="register"),
path("restaurant-create/",views.create_restaurant,name="restaurant-create"),
path("create-profile/",create_profile,name="create-profile"),
# path("search/",views.search_bar,name="search")
]
if settings.DEBUG:  
    urlpatterns+=static(settings.MEDIA_URL,
                        document_root =settings.MEDIA_ROOT)
    
