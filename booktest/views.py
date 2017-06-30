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




