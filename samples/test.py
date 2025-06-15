from cookiecutter.main import cookiecutter  # type: ignore
import shutil

configs = [
    {
        'project_slug': 'base',
    },
    {
        'project_slug': 'with_sdl',
        'use_sdl': 'yes'
    }
]

for config in configs:
    shutil.rmtree(config['project_slug'])

# intended, loops twice because i like to clear out first

for config in configs:
    cookiecutter(
        '..',
        no_input=True,
        extra_context=config,
    )
