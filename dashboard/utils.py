week = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
    7: 'Воскресенье'
}


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
