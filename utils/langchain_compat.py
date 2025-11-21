"""Compatibility shim for LangChain Tool API differences across versions.

Defines a minimal `Tool` class with `from_function` to be used when
`langchain.tools.Tool` is unavailable in the environment.
"""
try:
    from langchain.tools import Tool as LC_Tool
    Tool = LC_Tool
except Exception:
    class Tool:
        def __init__(self, func=None, name: str | None = None, description: str | None = None):
            self.func = func
            self.name = name
            self.description = description

        @classmethod
        def from_function(cls, func, name: str | None = None, description: str | None = None):
            return cls(func=func, name=name, description=description)

        def __repr__(self):
            return f"<Tool name={self.name} desc={self.description}>"
