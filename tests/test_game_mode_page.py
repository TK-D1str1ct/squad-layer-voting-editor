from streamlit.testing.v1 import AppTest
from pages.home_page import home_page
from pages.import_page import import_page
from pages.global_page import global_page
from pages.gamemode_page import gamemode_page
from pages.map_page import map_page
from pages.layer_page import layer_page
from pages.download_page import download_page
import pytest

import App_Utils as au


def render_gamemode_page():
    from pages.gamemode_page import gamemode_page

    gamemode_page()


@pytest.fixture()
def gamemode_app():
    app = AppTest.from_function(render_gamemode_page)

    au.init_session(app.session_state)

    page_order = [
        home_page,
        import_page,
        global_page,
        gamemode_page,
        map_page,
        layer_page,
        download_page,
    ]

    app.session_state.PAGE_ORDER = page_order

    yield app


def test_gamemode_page_renders(gamemode_app):
    app = gamemode_app
    app.run()

    assert not app.exception

    assert app.title[0].value == "🎮 Gamemode Exclusion Settings"


def test_gamemode_page_frames(gamemode_app):
    app = gamemode_app
    app.run()

    assert not app.exception

    print(f"dfs={app.dataframe[0].value}")
