import flet as ft

class Top(ft.View):
    def __init__(self):
        data = "Top data"
        controls = [
            ft.AppBar(title=ft.Text("Top view"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.TextField(value=data, on_change=self.changed),
            ft.ElevatedButton("Go to View1", on_click=self.clicked)
        ]
        super().__init__("/", controls=controls)
        self.data = data
        
    def clicked(self, e):
        e.page.go("/view1")
    
    def changed(self, e):
        self.data = e.control.value
        self.update()


class View1(ft.View):
    def __init__(self, _data):
        data = 'View1 data'
        controls = [
            ft.AppBar(title=ft.Text("View1"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text(f'Top\'s data: {_data}'),
            ft.TextField(value=data, on_change=self.changed),
            ft.ElevatedButton("Go to View2", on_click=self.clicked)
        ]
        super().__init__("/view1", controls=controls)
        self.data = data
        
    def clicked(self, e):
        e.page.go("/view2")
    
    def changed(self, e):
        self.data = e.control.value
        self.update()


class View2(ft.View):
    def __init__(self, _data):
        controls = [
            ft.AppBar(title=ft.Text("View2"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text(f'View1\'s data: {_data}'),
            ft.ElevatedButton("Go to Top", on_click=self.clicked)
        ]
        super().__init__("/view2", controls)
        
    def clicked(self, e):
        e.page.go("/")


def main(page: ft.Page):
    page.title = "test app"

    pop_flag = False

    def route_change(e):
        nonlocal pop_flag

        if pop_flag:
            pop_flag = False
        else:
            if page.route == "/":
                page.views.clear()
                page.views.append(
                    Top()
                )
            elif page.route == "/view1":
                page.views.append(
                    View1(page.views[-1].data)
                )
            elif page.route == "/view2":
                page.views.append(
                    View2(page.views[-1].data)
                )
        
    def view_pop(e):
        nonlocal pop_flag
        pop_flag = True
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.views.clear()
    page.go("/")


if __name__ == '__main__':
    ft.app(target=main)