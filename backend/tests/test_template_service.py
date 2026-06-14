from app.modules.templates.services.template_service import TemplateService


def test_template_rendering_supports_variables_conditionals_loops():
    service = TemplateService()
    output = service.render(
        """
        {% if user %}
        Hello {{ user.name }}
        {% for item in items %}{{ item }} {% endfor %}
        {% endif %}
        """,
        {"user": {"name": "Jane"}, "items": ["one", "two"]},
    )
    assert "Hello Jane" in output
    assert "one" in output and "two" in output
