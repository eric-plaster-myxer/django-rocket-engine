
def setup_env():
    """
    assume we are running with the correct setting - some commands will enforce
    explicit --setting.

    Always generate a new app.yaml by instanciating the template
    """
    import os
    import glob
    import subprocess
    from django.conf import settings

    from django.template import Template, Context

    version = subprocess.check_output(['git', 'describe'])
    with open(os.path.join(settings.BASE_DIR, 'VERSION'), 'w') as f:
        f.write(version)

    settings_name = os.environ['DJANGO_SETTINGS_MODULE'].rsplit('.', 1)[-1]
    env_name = getattr(settings, 'ENV_NAME', settings_name)

    context = {
            'env_name': env_name,
            'settings_name': settings_name,
            'version': version.replace('.', '-').replace('/', '-'),
            'tmp': os.environ.get('TMP', ''),
            }
    for tmpl_name in glob.glob(os.path.join(settings.BASE_DIR, '*.template.yaml')):
        with open(tmpl_name, 'r') as template:
            with open(os.path.join(settings.BASE_DIR,
                            '{}.yaml'.format(os.path.basename(tmpl_name).split('.')[0])),
                'w') as target:
                target.write(Template(template.read()).render(Context(context)))


setup_env()
