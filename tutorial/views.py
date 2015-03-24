# Third Party Stuff
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    forget,
    remember
)
from pyramid.view import view_config
from models.auth import User
from db_process.users_query import UserQuery
# IMAX Stuff
#from imax.forms.auth import SetPasswordForm


@view_config(route_name='home', renderer='template/home.pt')
def home(self):
    return {'name': 'Home View'}

#Todo: have to fix this. It is not working.
def includeme(config):
    #config.add_request_method(get_authenticated_user, 'user', reify=True)
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signin', '/signin')
    config.add_route('auth_change_password', '/auth/change-password')

@view_config(
    route_name='login',
    renderer='template/login.html',)
def login_view(self, request):
    next = request.params.get('next') or request.route_url('home')
    context = {}
    if request.method == "POST":
        email_id = request.POST.get('email_id', '')
        password = request.POST.get('password', '')
        context.update(email_id=email_id)
        usr = UserQuery()
        user = usr.get_user(email_id)
        if user:
            if user.check_password(password):
                if user.is_active is True:
                    headers = remember(request, '{0} {1}'.format(user.first_name, user.last_name))
                    return HTTPFound(location=next, headers=headers)
                else:
                    context.update(inactive_user=True)
            else:
                context.update(invalid_password=True)
        else:
            context.update(invalid_username=True)

    context.update({
        'next': next,
    })
    return context

@view_config(
    route_name='signin',
    renderer='template/signin.html',)
def signin_view(self, request):
    next = request.params.get('next') or request.route_url('home')
    context = {}
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email_id = request.POST.get('email_id', '')
        password = request.POST.get('password', '')
        user_category = request.POST.get('user_category', '')
        new_user = User(first_name, last_name, email_id, user_category, password)
        if UserQuery().is_email_id_already_registered(email_id):
            context.update(email_id_already_registered=True)
        else:
            UserQuery().add_user(new_user)


    context.update({'next': next, })
    print "Adding Users to Database." + str(context.get('next'))
    return context

@view_config(
    route_name='logout',
)
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)

