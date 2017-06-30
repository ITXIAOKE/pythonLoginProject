##1，创建项目test04

![这里写图片描述](http://img.blog.csdn.net/20170629135140973?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##2，创建应用app为booktest

![这里写图片描述](http://img.blog.csdn.net/20170629135201030?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##3，注册应用booktest
>作用让创建的应用运行起来

![这里写图片描述](http://img.blog.csdn.net/20170629135219782?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##4，在项目根目录下创建模板templates目录
+ 作用就是存放html文件

![这里写图片描述](http://img.blog.csdn.net/20170629135237469?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

+ 在项目的settings.py文件中配置模板，如下图：

![这里写图片描述](http://img.blog.csdn.net/20170629135251692?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##5，在项目根目录下创建static目录
+ 作用就是存放css/图片/js等文件

![这里写图片描述](http://img.blog.csdn.net/20170629135311384?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

+ 在项目的settings.py文件中配置static文件，如下图

![这里写图片描述](http://img.blog.csdn.net/20170629135322315?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##6，数据库的创建与配置

![这里写图片描述](http://img.blog.csdn.net/20170629135337940?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

手动的在mysql数据库中创建test04数据库，如下图

![这里写图片描述](http://img.blog.csdn.net/20170629135423747?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##7，DEBUG开关设置

![这里写图片描述](http://img.blog.csdn.net/20170629135455983?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##8，设置编码和时间

```
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'
```

##9，项目的urls文件中配置如下：

```
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('booktest.urls'))
]
```

##10，在booktest应用下创建urls目录并配置

```
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

```
##11，在booktest应用views中创建各个视图函数


```
from django.shortcuts import render
from django.http import JsonResponse
# PIL是python2版本的图像处理库，不过现在用Pillow比PIL强大，是python3的处理库
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
# 在python2.x中导入模块方法：
# from StringIO import String
# 在python2.x中它还有个孪生兄弟，运行速度比它快，用c实现的
# from cStringIO import StringIO

# 在python3.x中，StringIO已经在io模块中了，导入方法
from io import BytesIO


# ajax登录视图函数
def login_ajax(request):
    return render(request, 'booktest/login_ajax.html')


# ajax登录校验回调视图函数
def login_ajax_check(request):
    # 1，获取用户输入的用户名和密码
    uname = request.POST.get('uname')
    password = request.POST.get('password')
    # 获取用户输入的验证码
    vcode = request.POST.get('vcode')
    # 获取session中的验证码
    vcode_session = request.session.get('verifycode')

    # 2,用户名和密码校验
    if uname == 'xiaoke' and password == '123456' and vcode == vcode_session:
        # 保存用户的登录状态
        request.session['isLogin']=True
        request.session['uname']=uname
        request.session['password']=password
        return JsonResponse({'msg': 'ok'})
    elif uname != 'xiaoke' or password != '123456':
        return JsonResponse({'msg': 'fail_user'})
    elif vcode != vcode_session:
        return JsonResponse({'msg': 'fail_verify'})


def verify_code(request):
    # 1，定义变量，用于画面的背景色、宽、高
    # random.randrange(20, 100)意思是在20到100之间随机找一个数
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 2，创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 3，创建画笔对象
    draw = ImageDraw.Draw(im)
    # 4，调用画笔的point()函数绘制噪点，防止攻击
    for i in range(0, 100):
        # 噪点绘制的范围
        xy = (random.randrange(0, width), random.randrange(0, height))
        # 噪点的随机颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制出噪点
        draw.point(xy, fill=fill)
    # 5，定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 6，随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 7，构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 8，构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 9，绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 9，用完画笔，释放画笔
    del draw
    # 10，存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 11，内存文件操作
    buf = BytesIO()
    # 12，将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 13，将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# ajax登录成功视图函数
def success(request):
    # 用户已经登录
    if request.session.get('isLogin'):
        return render(request, 'booktest/success.html')
    else:
        return redirect('/login_ajax/')

# 发帖操作视图函数
def post_article(request):
    # 获取登录的用户名
    uname = request.session.get('uname')
    # 获取帖子的标题
    title = request.POST.get('title')
    content = request.POST.get('content')
    return HttpResponse('%s发了一篇名为%s的帖子：%s' % (uname.encode('utf-8').decode('utf-8'),
                        title.encode('utf-8').decode('utf-8'),content.encode('utf-8').decode('utf-8')))

```

##12，ajax登录页面布局代码如下：
+ csrf_token 的目地是为了防止csrf公积，django默认打开csrf：如下代码
+ 'django.middleware.csrf.CsrfViewMiddleware',
+ 查看网页源代码可知，csrf的键和值，所以请求的时候要携带，否则django直接禁止：

![这里写图片描述](http://img.blog.csdn.net/20170630142756506?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

+ ajax登录页面具体布局如下：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录页面</title>
    <script src="/static/js/jquery-1.12.4.min.js"></script>
    <style>
        #errorMsg {
            display: none;
            color: red;
        }
    </style>
    <script>
        $(function () {

            $('#btnLogin').click(function () {
                $('uname').reset;

                csrf = $('input').val();
                uname = $('#uname').val();
                password = $('#password').val();
                vcode = $('#vcode').val();

                //发起ajax请求，注意csrf攻击
                $.post('/login_ajax_check/', {
                    'csrfmiddlewaretoken': csrf,
                    'uname': uname,
                    'password': password,
                    'vcode': vcode,
                }, function (data) {
                    //获取返回的数据并进行操作
                    if (data.msg === 'ok') {
                        //登录成功
                        location.href = '/success/' //跳转到成功页面
                    } else if (data.msg === 'fail_user') {
                        $('#errorMsg').show().text('亲！用户名或密码错误！')

                    } else if (data.msg === 'fail_verify') {
                        //验证码错误
                        $('#errorMsg').show().text('亲！验证码错误！')
                    }
                })
            });
        });

    </script>
</head>

<body>

<div>
    {% csrf_token %}
    用户名：<input type="text" id="uname"><br/>
    密&nbsp;&nbsp;码：<input type="password" id="password"><br/>

    验证码：<input type="text" id="vcode"/><br/>
    <!--直接调用生产图片验证码的视图函数，生产验证码-->
    <img src="/verify_code/" id="imgvcode"/><br/>

    <input type="button" value="登录" id="btnLogin"><br/>
    <div id="errorMsg"></div>
</div>

</body>
</html>
```

##13，登录成功页面，进行发帖布局代码如下：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录成功，发帖页面</title>
</head>
<body>

<h2>亲！你登录成功了，欢迎你！！！</h2>
<form method="post" action="/post_article/">
    {% csrf_token %}
    标题:<input type="text" name="title"/><br/>
    内容:<textarea name="content"></textarea><br/>
    <input type="submit" value="发帖"/>
</form>
</body>
</html>

```

##14，执行迁移，生成session表

+ session表示需要执行迁移后，才会在mysql数据库中生成

![这里写图片描述](http://img.blog.csdn.net/20170630140201578?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


##15，查看mysql数据库

+ show tables;查看数据库test04中的表
+ django_session就是session表

![这里写图片描述](http://img.blog.csdn.net/20170630140242330?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

![这里写图片描述](http://img.blog.csdn.net/20170630140300575?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

+ desc django_session;查看session表结构:
+ 有session的键、值和过期时间

![这里写图片描述](http://img.blog.csdn.net/20170630140312890?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##16，开始登录测试

+ 输入用户名、密码和验证码

![这里写图片描述](http://img.blog.csdn.net/20170630140638785?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

+ 这是登录成功后的页面，进行发帖

![这里写图片描述](http://img.blog.csdn.net/20170630140700375?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

+ 这是发帖页面

![这里写图片描述](http://img.blog.csdn.net/20170630140711375?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

##17，查看数据库中session表

![这里写图片描述](http://img.blog.csdn.net/20170630140741918?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

查看Cookie中的sessionid值为“hzlqkmdkn6461kfwfm2oj7p5889o2fo1”，数据表中session的键为“hzlqkmdkn6461kfwfm2oj7p5889o2fo1”，是一样的，这样，服务器就可以在众多的请求者中找到对应的Session数据。

![这里写图片描述](http://img.blog.csdn.net/20170630142412821?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

在MySQL数据库命令行中复制值，在Base64解码中进行解码查看如下图。

![这里写图片描述](http://img.blog.csdn.net/20170630140754383?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxNDc0NTE5NA==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
