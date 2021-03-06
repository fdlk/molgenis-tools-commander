import pytest

from tests.integration.loader_mock import get_resource_folder
from tests.integration.utils import run_commander


@pytest.mark.integration
def test_add_theme(session):
    run_commander('add logo logo_blue')

    settings = session.get('sys_set_app')[0]
    assert settings['logo_href_navbar'] == '/logo/logo_blue.png'


@pytest.mark.integration
def test_add_theme_from_path(session):
    file = str(get_resource_folder().joinpath('logo_black.png'))
    run_commander('add logo --from-path {}'.format(file))

    settings = session.get('sys_set_app')[0]
    assert settings['logo_href_navbar'] == '/logo/logo_black.png'
