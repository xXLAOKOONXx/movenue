class Page:
    def __init__(self) -> None:
        self._master_is_set = False

    @property
    def master_is_set(self):
        return self._master_is_set

    def set_master(self, master):
        self.master = master
        self._master_is_set = True

    def get_ui_element(self):
        return self.frame