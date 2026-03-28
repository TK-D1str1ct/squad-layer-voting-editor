from streamlit.testing.v1 import AppTest


def test_app_renders_home_page():
    app = AppTest.from_file("app.py")

    app.run()

    assert not app.exception
    assert app.title[0].value == "Home"
