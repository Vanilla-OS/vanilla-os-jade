pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'vanilla_os_jade')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('pkgdatadir', pkgdatadir)
configure_file(
            input: 'vanilla-os-jade.in',
           output: 'vanilla-os-jade',
    configuration: conf,
          install: true,
      install_dir: get_option('bindir')
)

vanilla_os_jade_sources = [
    '__init__.py',
    'main.py',
    'parser.py'
]

install_data(vanilla_os_jade_sources, install_dir: moduledir)
