from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
#        users = Users.objects.all()[:15]
        return render(request, 'statuses/index.html', context={
            'name': _('Statuses'),
#            'users': users,
        })
