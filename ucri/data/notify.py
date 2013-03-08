from functools import wraps
from datetime import datetime
from flask.ext.login import current_user
from ucri.models.user import User
from ucri.models.notification import Notification

def notify(fn):
    '''
    This decoration requires the login_required decoration
    If you decorate an action with this, it will send all the users following the current user
    A notfication of the action assumed for pins
    '''
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        date = datetime.now()
        msg = "%s: " % (current_user.uname)
        # Function does not have a _
        if fn.__name__.find('_') == -1:
            msg += "%sed a picture" % fn.__name__
        elif 'edit_pin' ==  fn.__name__ or 'delete_pin' == fn.__name__ or fn.__name__ == 'add_comment':
            msg += "$sed a %s" % (fn.__name__.split('_'))
        else:
            msg += "updated their %s %s" % (fn.__name__.split('_'))
        notification = Notification(notifier=current_user.uname,
                        msg=msg,
                        date=date)
        for usr in current_user.follower_array:
            usr.notification_array.append(notification)
            usr.save()
        return fn(*args, **kwargs)
    return decorated_view
