class ExtraContextMixin:
    template_title = None
    btn_submit_title = None
    extra_context = {}

    def __init__(self):
        if self.template_title:
            self.extra_context['template_title'] = self.template_title
        if self.btn_submit_title:
            self.extra_context['btn_submit_title'] = self.btn_submit_title

    def get_mixin_context(self, context, **kwargs):
        context['default_user_image'] = None
        context.update(kwargs)
        return context
