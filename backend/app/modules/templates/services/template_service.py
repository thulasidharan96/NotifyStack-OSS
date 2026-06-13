from jinja2 import Environment, StrictUndefined

env = Environment(undefined=StrictUndefined, autoescape=True)


class TemplateService:
    def render(self, template: str, context: dict[str, object]) -> str:
        compiled = env.from_string(template)
        return compiled.render(**context)
