# .. -*- mode: python -*-
#
# ****************
# enki-sphinx.spec
# ****************
# This file instructs Pyinstaller to build a binary containing both Enki,
# Pylint, and Sphinx executables.
#
# Procedure to create this file:
#
# #. Run ``win\build_exe.bat`` and test. This creates working
#    ``enki.spec``, ``pylint.spec`` and ``sphinx-build.spec`` files.
# #. Combine these files according to the `Pyinstaller merge docs
#    <http://htmlpreview.github.io/?https://github.com/pyinstaller/pyinstaller/blob/develop/doc/Manual.html#multipackage-bundles>`_.
#    These steps are illustrated in the comments below.
# #. Run ``win\build_exe.bat`` again; the third build is the combined version.
#
# Imports
# =======
import os.path
import pylint
#
# Analysis
# ========
# Per the `Pyinstaller merge docs`_, first create uniquely-named analysis
# objects for both programs.
enki_a = Analysis(['bin/enki'],
  pathex=['.'],
  hiddenimports=[],
  hookspath=['win'],
  runtime_hooks=['win/rthook_pyqt4.py'])

sphinx_a = Analysis(['win/sphinx-build.py'],
  pathex=['.'],
  hiddenimports=['CodeChat'],
  hookspath=['win'],
  runtime_hooks=[])

# Provide the OS-dependent location of pylint's __main__.py file.
pylint_a = Analysis([os.path.join(pylint.__path__[0], '__main__.py')],
  pathex=['.'],
  hiddenimports=[],
  hookspath=None,
  runtime_hooks=None)
#
# Merge
# =====
# Next, eliminate duplicate libraries and modules. Listing Enki first seems to
# place all libraries and modules there.
MERGE(
    (enki_a, 'enki', 'enki'),
    (sphinx_a, 'sphinx', 'sphinx'),
    (pylint_a, 'pylint', 'pylint'),
    )
#
# Produce binaries
# ================
# Finally, produce the binaries. Note that the resulting Sphinx binary doesn't
# work as is, since it has no libraries bundled with it. Instead, it needs to
# be copied to the Enki directory before being executed.
enki_pyz = PYZ(enki_a.pure)
enki_exe = EXE(enki_pyz,
  enki_a.scripts,
  exclude_binaries=True,
  name='enki',
  debug=False,
  strip=None,
  upx=True,
  console=False,
  icon='icons/logo/enki.ico')
enki_coll = COLLECT(enki_exe,
  enki_a.binaries,
  enki_a.zipfiles,
  enki_a.datas,
  strip=None,
  upx=True,
  name='enki')

sphinx_pyz = PYZ(sphinx_a.pure)
sphinx_exe = EXE(sphinx_pyz,
  sphinx_a.scripts,
  exclude_binaries=True,
  name='sphinx-build',
  debug=False,
  strip=None,
  upx=True,
  console=True)
sphinx_coll = COLLECT(sphinx_exe,
  sphinx_a.binaries,
  sphinx_a.zipfiles,
  sphinx_a.datas,
  strip=None,
  upx=True,
  name='sphinx-build')

pylint_pyz = PYZ(pylint_a.pure)
pylint_exe = EXE(pylint_pyz,
  pylint_a.scripts,
  exclude_binaries=True,
  # TODO: This fails on Unix, since there's already a directory named
  # pylint/, conflicting with the binary this is producing named pylint.
  # One solution: change the name below. But then Enki needs to know
  # about this special case (unique name only for Linux frozen), which
  # is ugly.
  name='pylint',
  debug=False,
  strip=None,
  upx=True,
  console=True)
pylint_coll = COLLECT(pylint_exe,
  pylint_a.binaries,
  pylint_a.zipfiles,
  pylint_a.datas,
  strip=None,
  upx=True,
  name='pylint')

