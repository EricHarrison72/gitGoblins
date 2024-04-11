# ---------------------------------------------------
# test_jinja_macros.py
'''
Contains unit tests for jinja macros, which are
kind of like functions and warrant testing. 
Specifically tested here are the macros are in 
'helpers/selectors.html.jinja'.
'''
# --------------------------------------------------
import pytest
import jinja2
import os

# ------------
# FIXTURES

@pytest.fixture()
def template_name():
    file_name = "test_macros.html.jinja"
    yield file_name

    if os.path.exists(file_name):
        os.remove(file_name)

# ----------
# TESTS

# select_date tests [
def test_select_date_defaults(template_name):
    rendered = get_rendered_template(
        "{{ selectors.select_date() }}",
        template_name
    )

    default_div_id = 'dateSelect'
    assert ((f"<div id='{default_div_id}'" in rendered) or
            (f'<div id="{default_div_id}"' in rendered))

    default_ids = ['yearSelect', 'monthSelect', 'daySelect']
    for id in default_ids:
        assert any(f'<select id="{id}"' in segment for segment in rendered.split('>')) or \
               any(f"<select id='{id}'" in segment for segment in rendered.split('>'))

    default_selected_date = ['2017', '6', '24']
    for value in default_selected_date:
        assert ((f'<option value="{value}"  selected' in rendered) or
                (f"<option value='{value}'  selected" in rendered))

def test_select_date_params(template_name):
    rendered = get_rendered_template(
        "{{ selectors.select_date(id_prefix='goblin_', url_arg_date='2009-04-17') }}",
        template_name
    )

    expected_div_id = 'goblin_dateSelect'
    assert ((f"<div id='{expected_div_id}'>" in rendered) or
            (f'<div id="{expected_div_id}">' in rendered))

    expected_ids = ['goblin_yearSelect', 'goblin_monthSelect', 'goblin_daySelect']
    for id in expected_ids:
        assert ((f"<select id='{id}'" in rendered) or 
                (f'<select id="{id}"' in rendered))

    expected_selected_date = ['2009', '4', '17']
    for value in expected_selected_date:
        assert ((f'<option value="{value}"  selected >' in rendered) or
                (f"<option value='{value}'  selected >" in rendered))


# ] select location tests [
def test_select_single_location_defaults(template_name):
    rendered = get_rendered_template(
        "{{ selectors.select_single_location() }}",
        template_name
    )

    default_id = 'citySelect'
    assert ((f"<select id='{default_id}' " in rendered) or
            (f'<select id="{default_id}" ' in rendered))

    default_selected_city_id = '10' # for Canberra
    assert f'<option value="{default_selected_city_id}"  selected >' in rendered

def test_select_single_location_params(template_name):
    rendered = get_rendered_template(
        "{{ selectors.select_single_location(url_arg_city='AliceSprings') }}",
        template_name
    )

    expected_selected_city_id = '4' # for Alice Springs
    assert f'<option value="{expected_selected_city_id}"  selected >' in rendered

# ] select statistic tests [
def test_select_stat_defaults(template_name):
    rendered = get_rendered_template(
        "{{ selectors.select_stat() }}",
        template_name
    )

    default_id = 'statSelect'
    assert ((f"<select id='{default_id}' " in rendered) or
            (f'<select id="{default_id}" ' in rendered))

    default_selected_stat_id = '0' # for temperature
    assert f'<option value="{default_selected_stat_id}"  selected >' in rendered

def test_select_stat_params(template_name):
    rendered = get_rendered_template(
        "{{ selectors.select_stat(url_arg_stat='wind') }}",
        template_name
    )

    expected_selected_stat_id = '1' # for wind
    assert f'<option value="{expected_selected_stat_id}"  selected >' in rendered

# ]---------------------------
# SOME HELPER FUNCTIONS
# (this just doesn't make sense as a fixture since it takes arguments)
def generate_html_file(test_html):
    html_file = open("tests/test_macros.html.jinja", "w")
    html_file.write('''
        <!-- this is a TEST file that is allowed to be deleted -->
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
        {% import 'helpers/selectors.html.jinja' as selectors %}
    ''')
    html_file.write(test_html)
    html_file.write('''
        </body>
        </html>
    ''')
    html_file.close()

# again, this doesn't make sense as a fixture
def get_rendered_template(test_html, file_name):
    generate_html_file(test_html)

    rendered = jinja2.Environment(
        loader=jinja2.FileSystemLoader(['tests','weatherApp/templates'] )
        ).get_template(file_name).render()

    print(rendered)
    return rendered