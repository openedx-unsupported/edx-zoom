"""
edx-zoom XBlock

Subclass of LtiConsumerXBlock
"""

import logging

from lti_consumer import LtiConsumerXBlock
from lti_consumer.utils import _
from web_fragments.fragment import Fragment
from xblock.core import Scope, String
from xblockutils.resources import ResourceLoader

from django.utils.functional import cached_property


log = logging.getLogger(__name__)


class ZoomXBlock(LtiConsumerXBlock):
    override_launch_url = String(
        display_name=_("Launch URL"),
        default='https://applications.zoom.us/lti/rich',
        scope=Scope.settings
    )

    lti_id = 'zoom'
    display_name = String(
        display_name=_("Display Name"),
        help=_(
            "Enter the name that students see for this component. "
            "Analytics reports may also use the display name to identify this component."
        ),
        scope=Scope.settings,
        default=_("Zoom"),
    )
    description = String(
        display_name=_("Application Information"),
        help=_(
            "Enter a description of your use of Zoom. "
        ),
        default=_("Use Zoom to host office hours and other course meetings"),
        scope=Scope.settings
    )
    block_settings_key = 'edx_zoom'

    editable_fields = (
        'display_name', 'description', 'custom_parameters', 'override_launch_url',
        'inline_height', 'modal_height', 'modal_width'
    )
    ask_to_send_username = ask_to_send_email = True
    has_author_view = True


    @cached_property
    def launch_settings(self):
        from .models import LTICredential
        log.info('getting key and secret for %s', self.course_id)
        try:
            cred = LTICredential.objects.get(course_id=self.course_id)
            course_settings = {'key': cred.key, 'secret': cred.secret, 'url': cred.launch_url, 'managed': True}
        except LTICredential.DoesNotExist:
            course_settings = getattr(self.course, 'zoom_settings', {})
            course_settings['managed'] = False
        if not course_settings.get('url', ''):
            course_settings['url'] = self.override_launch_url
        return course_settings

    @cached_property
    def lti_provider_key_secret(self):
        """
        Obtains client_key and client_secret credentials from current course.
        """
        log.info('getting key and secret for %s', self.course_id)
        creds = self.launch_settings
        return creds.get('key', None), creds.get('secret', None)

    @property
    def launch_url(self):
        return self.launch_settings['url']

    def _get_context_for_template(self):
        ctx = super()._get_context_for_template()
        ctx['missing_credentials'] = self.lti_provider_key_secret[0] is None
        ctx['ask_to_send_username'] = ctx['ask_to_send_email'] = True
        return ctx

    def student_view(self, context):
        fragment = Fragment()
        lti_loader = ResourceLoader('lti_consumer')
        loader = ResourceLoader(__name__)
        context = self._get_context_for_template()
        fragment.add_content(loader.render_mako_template('/templates/student.html', context))
        fragment.add_css(loader.load_unicode('static/css/student.css'))
        fragment.add_javascript(lti_loader.load_unicode('static/js/xblock_lti_consumer.js'))
        fragment.initialize_js('LtiConsumerXBlock')
        from .models import LaunchLog
        LaunchLog.update(self.runtime.user_id, self.location, self.launch_settings['managed'])
        return fragment

    def author_view(self, context):
        fragment = Fragment()
        loader = ResourceLoader(__name__)
        context.update(self._get_context_for_template())
        fragment.add_content(loader.render_mako_template('/templates/author.html', context))
        return fragment
