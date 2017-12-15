from django.shortcuts import HttpResponse,render,redirect
from django.conf.urls import url
from stark.service import v1
from app01 import models
from django.forms import ModelForm
class UserInfoModelForm(ModelForm):
    class Meta:
        model=models.UserInfo
        fields="__all__"
        error_messages={
            'name':{
                'required':'用户名不能为空'
            }
        }
class UserInfoConfig(v1.StarkConfig):
       list_display = ['id','name']

       show_add_btn = True
       model_form_class = UserInfoModelForm
       # def extra_url(self):
       #     url_list=[
       #         url(r'^xxxXX$',self.func),
       #     ]
       #     return url_list
       # def func(self,request):
       #       return HttpResponse('......')

v1.site.register(models.UserInfo,UserInfoConfig)

class UserTypeConfig(v1.StarkConfig):
    list_display = ['name',]

v1.site.register(models.UserType,UserTypeConfig)

class RoleConfig(v1.StarkConfig):
    list_display = ['id','xxx']

    def delete_view(self, request, nid):
        if request.method == "GET":
            return render(request, "stark/delete.html")
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())
v1.site.register(models.Role,RoleConfig)




class HostModelForm(ModelForm):
    class Meta:
        model = models.Host
        fields = ['id','hostname','ip','port']
        error_messages = {
            'hostname':{
                'required':'主机名不能为空',
            },
            'ip':{
                'required': 'IP不能为空',
                'invalid': 'IP格式错误',
            }

        }

class HostConfig(v1.StarkConfig):
    def ip_port(self, obj=None, is_header=False):
        if is_header:
            return '自定义列'
        return "%s:%s" % (obj.ip, obj.port,)

    list_display = ['id', 'ip', 'hostname', 'port',ip_port]



    show_add_btn = True
    model_form_class = HostModelForm


    def extra_url(self):
        urls = [
            url('^report/$', self.report_view)
        ]
        return urls

    def report_view(self, request):
        return HttpResponse('自定义报表')

v1.site.register(models.Host,HostConfig)



