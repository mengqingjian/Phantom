from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse,render,redirect
class StarkConfig(object):
      #1.定制页面显示的列
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' %(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return '编辑'
        return mark_safe('<a href="%s">编辑</a>' %(self.get_chang_url(obj.id),))
    def delete(self,obj=None,is_header=False):
        if is_header:
            return '删除'
        return mark_safe('<a href="%s">删除</a>' %(self.get_delete_url(obj.id),))
    list_display = []
    def get_list_display(self):
        data=[]
        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        return data

     #2.是否显示添加按钮
    show_add_btn=True
    def get_show_add_btn(self):
        return self.show_add_btn

    #3.model_form_class
    model_form_class=None
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class
        from django.forms import ModelForm
        # class add_ModeForm(ModelForm):
          # def Meta(self):
          #     model = self.model_class
          #     fields = "__all__"
        meta=type('Meta',(object,),{'model':self.model_class,'fields':"__all__"})
        add_ModeForm=type("add_ModeForm",(ModelForm,),{'Meta':meta})
        return add_ModeForm

    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site=site
    def get_urls(self):
        app_model_name=(self.model_class._meta.app_label,self.model_class._meta.model_name,)
        url_patterns=[
            url(r'^$',self.changlist_view,name="%s_%s_changlist"%app_model_name),
            url(r'^add/$',self.add_view,name="%s_%s_add"%app_model_name),
            url(r'^(\d+)/delete/$', self.delete_view, name="%s_%s_delete" % app_model_name),
            url(r'^(\d+)/change/$', self.change_view, name="%s_%s_chang" % app_model_name),
        ]

        url_patterns.extend(self.extra_url())
        return url_patterns
    def extra_url(self):
        return []

    @property
    def urls(self):
        return self.get_urls()

    def get_chang_url(self,nid):
        name="stark:%s_%s_chang"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        edit_url=reverse(name,args=(nid,))
        return edit_url
    def get_add_url(self):
        name="stark:%s_%s_add"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        edit_url=reverse(name)
        return edit_url
    def get_delete_url(self,nid):
        name="stark:%s_%s_delete"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        edit_url=reverse(name,args=(nid,))
        return edit_url
    def get_list_url(self):
        name="stark:%s_%s_changlist"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        edit_url=reverse(name)
        return edit_url

#################处理请求的方式##############################
    def changlist_view(self,request,*args,**kwargs):
        #处理表头
        head_list=[]
        for filted_name in self.get_list_display():
            if isinstance(filted_name,str):
                # 根据类和字段名称，获取字段对象的verbose_name
                verbose_name=self.model_class._meta.get_field(filted_name).verbose_name
            else:
                verbose_name=filted_name(self,is_header=True)
        data_list = self.model_class.objects.all()
        #处理表中数据
        new_data_list = []
        for row in data_list:
            # row是 UserInfo(id=2,name='alex2',age=181)
            # row.id,row.name,row.age
            temp = []
            for field_name in self.get_list_display():
                if isinstance(field_name, str):
                    val = getattr(row,field_name)
                else:
                    val = field_name(self,row)
                temp.append(val)
            new_data_list.append(temp)

        return render(request, 'stark/changelist.html', {'data_list': new_data_list, 'head_list': head_list,'add_url':self.get_add_url(),'show_add_btn':self.get_show_add_btn()})
    #添加的数据及页面，用modelform
    def add_view(self, request, *args, **kwargs):
        model_form_class=self.get_model_form_class()
        if request.method=="GET":
            form=model_form_class()
            return render(request,"stark/add_view.html",{'form':form})
        else:
            form=model_form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, "stark/add_view.html", {'form': form})
    #修改数据及页面
    def change_view(self, request, nid, *args, **kwargs):
        obj=self.model_class.objects.filter(pk=nid).first()
        if not obj:
            redirect(self.get_list_url())
        model_form_class=self.get_model_form_class()
        if request.method=="GET":
            form=model_form_class(instance=obj)
            return render(request,"stark/change_view.html",{'form':form})
        else:
            form=model_form_class(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, "stark/change_view.html", {'form': form})
    def delete_view(self, request, nid):
        return HttpResponse(123)
        # self.model_class.objects.filter(pk=nid).delete()
        # return redirect(self.get_list_url())
class StarkSite(object):
    def __init__(self):
        self._registry = {}
    def register(self,model_class,stark_config_class=None):
        if not stark_config_class:
            stark_config_class=StarkConfig
        self._registry[model_class]=stark_config_class(model_class,self)

    def get_urls(self):
        url_pattern=[]

        for model_class,stark_config_obj in self._registry.items():
            """为每一个类，创建了4个url"""
            app_name=model_class._meta.app_label
            model_name=model_class._meta.model_name

            curd_url=url(r'^%s/%s/'%(app_name,model_name,),(stark_config_obj.urls,None,None))
            url_pattern.append(curd_url)
        return url_pattern
    @property
    def urls(self):
        return(self.get_urls(),None,'stark')


site=StarkSite()
