class Group:
    def __init__(self, name: str, group_vars: dict) -> None:
        self.name = name
        self.vars = dict() if group_vars is None else group_vars

    def members(self):
        return self.vars.get("members", list())

    def get_var(self, name: str):
        v = self.vars.get(name, None)
        return v
