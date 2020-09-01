from interactive_widgets_builder.view_controller import ViewController
from IPython.display import display, clear_output
from ipywidgets import widgets, Layout, VBox, HBox


class AuthenticationView():
    def _submit(self, b):
        if self.user_textbox.value == 'esb21375' and self.pwd_textbox.value == 'pwd':
            clear_output(wait=True)
            vc = ViewController(platform='jupyter')
            vc.entry()
        else:
            pass

    def __init__(self):
        self.user_textbox = widgets.Text(
            value='',
            placeholder='',
            description='User:',
            disabled=False,
            layout=Layout(width='94%', height='40px')
        )

        self.pwd_textbox = widgets.Password(
            value='',
            placeholder='',
            description='Password:',
            disabled=False,
            layout=Layout(width='50%', height='40px')
        )
        self.button = widgets.Button(
            value=False,
            description='Enter',
            disabled=False,
            button_style='',
            tooltip='',
            icon='Enter',
            layout=Layout(width='10%', height='80px')
        )
        self.button.on_click(self._submit)

    def display(self):
        display(HBox([
            VBox([self.user_textbox, self.pwd_textbox]),
            self.button
        ]))
