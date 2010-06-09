# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import include
from mailng.lib import events, parameters

def init():
    events.register("UserMenuDisplay", menu)
    events.register("UserLogin", userlogin)
    events.register("UserLogout", userlogout)
    parameters.register("webmail", "IMAP_SERVER", "string", "127.0.0.1",
                        help=_("Address of your IMAP server"))
    parameters.register("webmail", "IMAP_SECURED", "list_yesno", "no",
                        help=_("Use a secured connection to access IMAP server"))
    parameters.register("webmail", "IMAP_PORT", "int", "143",
                        help=_("Listening port of your IMAP server"))
    parameters.register("webmail", "SMTP_SERVER", "string", "127.0.0.1",
                        help=_("Address of your SMTP server"))
    parameters.register("webmail", "SMTP_PORT", "int", "25",
                        help=_("Listening port of your SMTP server"))
    parameters.register("webmail", "SMTP_AUTHENTICATION", "list_yesno", "no",
                        help=_("Server needs authentication"))
    parameters.register("webmail", "SMTP_SECURED", "list_yesno", "no",
                        help=_("Use a secured connection to access SMTP server"))

def destroy():
    events.unregister("UserMenuDisplay", menu)
    events.unregister("UserLogin", userlogin)
    parameters.unregister_app("webmail")

def infos():
    return {
        "name" : "Webmail",
        "version" : "1.0",
        "description" : _("Simple IMAP webmail")
        }

def urls():
    return (r'^mailng/webmail/',
            include('mailng.extensions.webmail.urls'))

def menu(**kwargs):
    import views

    if kwargs["target"] != "user_menu_box":
        return []
    return [
        {"name" : "webmail",
         "label" : _("Webmail"),
         "url" : reverse(views.index),
         "img" : "/static/pics/webmail.png"}
        ]

def userlogin(**kwargs):
    from imap_listing import IMAPconnector

    if kwargs["request"].user.id == 1:
        return
    m = IMAPconnector(user=kwargs["request"].user.username,
                      password=kwargs["password"])

def userlogout(**kwargs):
    from imap_listing import IMAPconnector

    if kwargs["request"].user.id == 1:
        return
    m = IMAPconnector(user=kwargs["request"].user.username)
    m.logout()