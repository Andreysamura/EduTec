import os
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.static.assets.images.slider.slider import Slider  # Importa el modelo del slider

@blueprint.route('/index')
@login_required
def index():
    slider_model = Slider()  # Instancia el modelo del slider
    images = slider_model.get_images()  # Obtén las imágenes del slider

    # Genera una lista de tuplas (índice, imagen) para el colapso
    images_with_index = [(index, image) for index, image in enumerate(images)]

    # Pasa las imágenes tanto para el slider como para el colapso al template
    return render_template('home/index.html', segment='index', slider_images=images, collapse_images=images_with_index)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
