gnome.compile_resources(
  'org.bredos.welcome',
  'org.bredos.welcome.gresource.xml',
  gresource_bundle: true,
  source_dir: meson.current_build_dir(),
  install_dir: join_paths(get_option('datadir'), 'welcome/data'),
  install: true
)


desktop_file = i18n.merge_file(
        input: 'org.bredos.welcome.desktop.in',
       output: 'org.bredos.welcome.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'org.bredos.welcome.appdata.xml.in',
       output: 'org.bredos.welcome.appdata.xml',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util, args: ['validate', appstream_file])
endif

install_data('org.bredos.welcome.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

install_data('ui/window.ui',
  install_dir: join_paths(get_option('datadir'), 'welcome/data/ui')
)


subdir('icons')
