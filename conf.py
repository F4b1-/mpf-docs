#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# sphinx-doc config file

import time
import os
import re
import sys

import git
import sphinx_rtd_theme

extensions = ['sphinx.ext.todo',
              'sphinx.ext.ifconfig']

source_suffix = '.rst'

master_doc = 'index'

version = '0.50+'  # all versions these docs cover
release = '0.50.x'  # latest release

project = 'Mission Pinball Framework v{} User Documentation'.format(version)
copyright = '2013-%s, The Mission Pinball Framework Team' % time.strftime('%Y')
author = 'The Mission Pinball Framework Team'

# dev warning box will be shown in HTML builds for the following GitHub branch
# names:
branches_for_dev_warning = ['dev']

language = None

exclude_patterns = ['_build',
                    '_not_updated_yet',
                    '_doc_tools',
                    '_src']

pygments_style = 'none'
highlight_language = 'yaml'

todo_include_todos = True

# Tests Links -------------------------------------------------------

mpf_examples = 'mpf_examples'
mpfmc_examples = 'mpfmc_examples'

# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# html_logo = None
html_favicon = '_static/images/icons/favicon.ico'
html_static_path = ['_static', 'examples']

# html_extra_path = []  # will be copied to root

html_last_updated_fmt = '%b %d, %Y'
htmlhelp_basename = 'MissionPinballFrameworkdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    'preamble': r'''
        \setcounter{secnumdepth}{0}
        \usepackage{bera}
        \usepackage[defaultsans]{lato}
        \usepackage{inconsolata}
        \usepackage{ragged2e}
        \AtBeginDocument{\raggedright}
        \setcounter{tocdepth}{1}
        \pagenumbering{arabic}
        \renewcommand{\labelitemi}{$\bullet$}
        \renewcommand{\labelitemii}{$\bullet$}
        \renewcommand{\labelitemiii}{$\bullet$}
        \renewcommand{\labelitemiv}{$\bullet$}

        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyhf{}
        \rhead{\thepage}
        \lhead{{\leftmark} ({\nouppercase{\rightmark}})}
        \renewcommand{\headrulewidth}{.4pt}

        ''',

    'figure_align': 'H',

    'releasename': 'Version',

    }

# Added "True" at the end to make Layex only use the TOC from index.rst
# and not the other text content
latex_documents = [
    (master_doc, 'MissionPinballFramework.tex',
     'Mission Pinball Framework Documentation',
     'The Mission Pinball Framework Team', 'report', True),
]

# latex_logo = '_static/images/mpf-logo-200.png'  # doesn't work with report class
# latex_use_parts = False
# latex_show_pagerefs = True
# latex_show_urls = 'inline'
# latex_appendices = []
# latex_domain_indices = True

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'missionpinballframework',
     'Mission Pinball Framework Documentation',
     [author], 1)
    ]

man_show_urls = True

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'MissionPinballFramework',
     'Mission Pinball Framework Documentation',
     author, 'MissionPinballFramework', 'Awesome Pinball Software.',
     'Miscellaneous'),
]

# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
epub_tocdepth = 2

# -- Show warnings for dev branches in HTML docs --------------------------

# If this is running on ReadTheDocs.org, the context dict will be overwritten
# by theirs which will contain the propoer branch name (since the git command
# doesn't work there.

context = dict()

try:
    context['github_version'] = git.Repo().active_branch.name
except TypeError:
    context['github_version'] = None


def setup(app):
    app.add_stylesheet('mpf.css')

    # We need to do this in the setup() function since ReadTheDocs will append
    # the context dict to the end of conf.py which means we don't have the
    # populated value at the global context yet, so we need to do it here.

    if globals()['context']['github_version'] in branches_for_dev_warning:

        globals()['rst_prolog'] = '''
        
        .. only:: html
        
           .. warning::
           
              **This is the dev documentation for an unreleased version of MPF!**
        
              This is the documentation for MPF |version|, which is the "dev" (next)
              release of MPF that is a work-in-progress. Unless you're specifically
              looking for this version, you probably want to use the version of
              documentation called "latest" which is for the latest released version of
              MPF. That documentation is at
              `docs.missionpinball.org/en/latest <http://docs.missionpinball.org/en/latest>`_.
        
        '''


def setup_tests_link(link_name, repo_name, package_name):
    try:
        os.unlink(link_name)
    except FileNotFoundError:
        pass

    if os.path.isdir(os.path.join(os.getcwd(), os.pardir, repo_name, package_name, 'tests', 'machine_files')):
        tests_root = os.path.join(os.getcwd(), os.pardir, repo_name, package_name, 'tests', 'machine_files')

    elif os.path.isdir(os.path.join(os.getcwd(), '_src', repo_name, package_name, 'tests', 'machine_files')):
        tests_root = os.path.join(os.getcwd(), '_src', repo_name, package_name, 'tests', 'machine_files')

    else:
        # clone repo
        print("Cloning {}".format(repo_name))
        current_branch = git.Repo().active_branch.name
        repo = git.Repo.clone_from("https://github.com/missionpinball/" + repo_name + ".git", os.path.join(os.getcwd(), '_src', repo_name), branch=current_branch)

        tests_root = os.path.join(os.getcwd(), '_src', repo_name, package_name, 'tests', 'machine_files')

    print("Creating '{}' link to {}".format(link_name, tests_root))
    os.symlink(tests_root, link_name)


def verify_version(version_file):

    #  http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
    verstrline = open(version_file, "rt").read()
    VSRE = r"^__short_version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        mpf_version_required_string = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (version_file,))

    if mpf_version_required_string != mpf._version.__short_version__:
        raise RuntimeError("mpf-examples version mismatch. MPF is version {} "
                           "but the mpf-examples repo found requires MPF {}".format(
            mpf._version.__short_version__, mpf_version_required_string))

setup_tests_link(mpf_examples, 'mpf', 'mpf')
setup_tests_link(mpfmc_examples, 'mpf-mc', 'mpfmc')
