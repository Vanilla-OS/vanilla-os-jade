pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
functionsdir = join_paths(pkgdatadir, 'vanilla_os_jade/functions')

vanilla_os_jade_sources = [
    '__init__.py',
    'base.py',
    'partitioning.py',
]

install_data(vanilla_os_jade_sources, install_dir: functionsdir)