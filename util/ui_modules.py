from tornado.web import UIModule

class UiModule(UIModule):
    def render(self, *args, **kwargs):
        return '我是 UI_Module'