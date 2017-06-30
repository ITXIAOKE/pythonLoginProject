from django.conf.urls import url
from  booktest import views

urlpatterns = [
    # 登录成功url
    url(r'^success/$', views.success),
    # ajax登录url
    url(r'^login_ajax/$', views.login_ajax),
    # ajax登录校验url
    url(r'^login_ajax_check/$', views.login_ajax_check),
    # 生产验证码图片url
    url(r'^verify_code/$', views.verify_code),
    # 发帖页面url
    url(r'^post_article/$', views.post_article),
]
