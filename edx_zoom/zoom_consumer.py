from __future__ import absolute_import, unicode_literals

import logging

from lti_consumer import LtiConsumerXBlock
from lti_consumer.utils import _
from web_fragments.fragment import Fragment
from xblock.core import List, Scope, String, XBlock
from xblock.fields import Boolean, Float, Integer
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
        default=_("Use Zoom to join office hours and other fun meetings"),
        scope=Scope.settings
    )
    lti_key = String(
        display_name=_("Application Key"),
        help=_(
            "Enter the LTI key you created on zoom.us"
        ),
        default="",
        scope=Scope.settings
    )
    lti_secret = String(
        display_name=_("Application Secret"),
        help=_(
            "Enter the LTI secret you created on zoom.us"
        ),
        default="",
        scope=Scope.settings
    )
    block_settings_key = 'edx_zoom'

    editable_fields = (
        'display_name', 'description', 'custom_parameters', 'override_launch_url',
        'lti_key', 'lti_secret', 'inline_height',
        'modal_height', 'modal_width'
    )
    ask_to_send_username = ask_to_send_email = True


    @cached_property
    def model_settings(self):
        from .models import LTICredential
        log.info('getting key and secret for %s', self.course_id)
        try:
            cred = LTICredential.objects.get(course_id=self.course_id)
        except LTICredential.DoesNotExist:
            cred = None
        return cred

    @cached_property
    def lti_provider_key_secret(self):
        """
        Obtains client_key and client_secret credentials from current course.
        """
        if self.lti_key and self.lti_secret:
            creds = (self.lti_key, self.lti_secret)
            log.info("using key from xblock %s", self.location)
        else:
            log.info('getting key and secret for %s', self.course_id)
            creds = self.model_settings
            if creds:
                creds = creds.key, creds.secret
            else:
                creds = None, None
        return creds

    @property
    def launch_url(self):
        creds = self.model_settings
        if creds:
            return creds.launch_url
        else:
            return self.override_launch_url

    def _get_context_for_template(self):
        ctx = super(ZoomXBlock, self)._get_context_for_template()
        ctx['missing_credentials'] = self.lti_provider_key_secret[0] is None
        ctx['ask_to_send_username'] = ctx['ask_to_send_email'] = True
        try:
            ctx['is_studio'] = self.runtime.service(self, 'completion') is None
        except Exception:
            ctx['is_studio'] = True
        return ctx

    def student_view(self, context):
        fragment = Fragment()
        lti_loader = ResourceLoader('lti_consumer')
        loader = ResourceLoader(__name__)
        context.update(self._get_context_for_template())
        fragment.add_content(loader.render_mako_template('/templates/student.html', context))
        fragment.add_css(loader.load_unicode('static/css/student.css'))
        fragment.add_javascript(lti_loader.load_unicode('static/js/xblock_lti_consumer.js'))
        fragment.initialize_js('LtiConsumerXBlock')
        return fragment
