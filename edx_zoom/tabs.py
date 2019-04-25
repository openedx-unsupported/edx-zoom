from django.utils.translation import ugettext_noop

from courseware.tabs import EnrolledTab


class ZoomTab(EnrolledTab):
    """
    The course progress view.
    """
    type = 'zoom'
    title = ugettext_noop('Meetings')
    priority = 40
    view_name = 'edx_zoom:launch'
    is_hideable = True
    is_default = True

    @classmethod
    def is_enabled(cls, course, user=None):
        return True
