import os
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.views.generic.base import RedirectView
from invoice.views import print_invoice
from attendance import urls as attendance_urls


urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),
    path('django-admin/', admin.site.urls),
    path('login/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('invoice/print/<str:invoice_number>/', print_invoice, name='print-invoice'),
    path('attendance/', include(attendance_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'media/', document_root=os.path.join(settings.MEDIA_ROOT, 'media'))
    urlpatterns += [
        path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'myapp/images/favicon.ico'))
    ]
