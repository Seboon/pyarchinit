# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
                             -------------------
        begin                : 2007-12-01
        copyright            : (C) 2008 by Luca Mandolesi; Enzo Cocca <enzo.ccc@gmail.com>
        email                : mandoluca at gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                       *
 ***************************************************************************/
"""
import shutil
import subprocess
import sys
from shlex import quote as shlex_quote
from importlib.metadata import distributions
import os
from os import path
import platform
try:
    # Tenta di importare pip
    import pip

except ImportError:
    if platform.system()=='Darwin':

        QGIS_PREFIX_PATH = '/Applications/QGIS.app/Contents/MacOS'  # Replace with your QGIS installation path
        python_executable = os.path.join(QGIS_PREFIX_PATH, 'bin', 'python3')

        # Se l'importazione fallisce, installa pip
        subprocess.call([python_executable, '-m', 'ensurepip'])

        # Aggiorna pip all'ultima versione
        subprocess.call([python_executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    elif platform.system()=='Windows':
        # Se l'importazione fallisce, installa pip
        subprocess.call(['python', '-m', 'ensurepip'])

        # Aggiorna pip all'ultima versione
        subprocess.call(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])

# Da questo punto in poi, puoi assumere che pip sia installato e aggiornato

from qgis.PyQt.QtCore import QObject,pyqtSignal,QThread
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QProgressBar, QTableWidget,
                                 QTableWidgetItem, QCheckBox, QHeaderView)
from qgis.core import QgsSettings
from .modules.utility.pyarchinit_OS_utility import Pyarchinit_OS_Utility
from .modules.utility.pyarchinit_folder_installation import pyarchinit_Folder_installation

def show_install_dialog(packages):
    dialog = InstallDialog(packages)
    dialog.exec_()
class Worker(QObject):
    finished = pyqtSignal()  # signal emitted when the worker is done
    progress = pyqtSignal(int)  # signal emitted to update the progress bar

    def install_packages(self, packages):
        total = len(packages)
        for i, package in enumerate(packages):
            self.progress.emit(int((i + 1) / total * 100))  # emit progress signal
            install(package)

        self.finished.emit()  # emit finished signal
class InstallDialog(QDialog):
    def __init__(self, packages):
        super().__init__()
        self.packages = packages
        self.initUI()

    def initUI(self):


        layout = QVBoxLayout()

        self.label = QLabel("Select packages to install:")
        layout.addWidget(self.label)

        self.table = QTableWidget(len(self.packages), 2)
        self.table.setHorizontalHeaderLabels(["Package", "Install"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, package in enumerate(self.packages):
            self.table.setItem(i, 0, QTableWidgetItem(package))
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.table.setCellWidget(i, 1, checkbox)


        layout.addWidget(self.table)

        self.install_button = QPushButton("Install Packages")
        self.install_button.clicked.connect(self.install_selected_packages)
        layout.addWidget(self.install_button)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.setLayout(layout)
        self.setWindowTitle("PyArchInit - Installazione pacchetti")
        self.set_icon(os.path.abspath(os.path.join(os.path.dirname(__file__), "logo_pyarchinit.png")))
        self.setGeometry(300, 300, 400, 300)
    def set_icon(self, icon_path):
        self.setWindowIcon(QIcon(icon_path))

    def install_selected_packages(self):
        selected_packages = []
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 1).isChecked():
                selected_packages.append(self.table.item(i, 0).text())

        if selected_packages:
            self.thread = QThread(self)
            self.worker = Worker()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(lambda: self.worker.install_packages(selected_packages))

            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.update_progress)  # connect progress signal to some slot
            self.worker.finished.connect(self.finish_install)  # connect finish signal to some slot

            self.thread.start()

    def update_progress(self, value):
        self.progress.setValue(value)
        self.label.setText(f"Installing package...")

    def finish_install(self):
        self.label.setText("Installation complete")
        self.accept()

#app = QApplication(sys.argv)


s = QgsSettings()
#L = QgsSettings().value("locale/userLocale")[0:2]
sys.path.append(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'resources')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'gui', 'ui')))

pyarchinit_home = os.path.expanduser("~") + os.sep + 'pyarchinit'
fi = pyarchinit_Folder_installation()
if not os.path.exists(pyarchinit_home):
    fi.install_dir()
else:
    os.environ['PYARCHINIT_HOME'] = pyarchinit_home

confing_path = os.path.join(os.sep, pyarchinit_home, 'pyarchinit_DB_folder', 'config.cfg')
logo_iccd = os.path.join(os.sep, pyarchinit_home, 'pyarchinit_DB_folder', 'logo.jpg')
if not os.path.isfile(confing_path):
    fi.installConfigFile(os.path.dirname(confing_path))

fi.installConfigFile(os.path.dirname(logo_iccd))


def is_osgeo4w():
    return 'OSGEO4W_ROOT' in os.environ

def get_osgeo4w_python():
    osgeo4w_root = os.environ.get('OSGEO4W_ROOT')
    if osgeo4w_root:
        return os.path.join(osgeo4w_root, 'bin', 'python-qgis.bat')
    return sys.executable



def install(package):


    #global result
    if platform.system() == 'Windows' and is_osgeo4w():
        python_executable = get_osgeo4w_python()
        subprocess.run([python_executable, "-m", "pip", "install", shlex_quote(package)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
    elif platform.system() == 'Windows':
        python_executable = 'python'
        subprocess.run([python_executable, "-m", "pip", "install", shlex_quote(package), "--user"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
    elif platform.system()=='Darwin':

        QGIS_PREFIX_PATH = '/Applications/QGIS.app/Contents/MacOS'  # Replace with your QGIS installation path
        python_executable = os.path.join(QGIS_PREFIX_PATH, 'bin', 'python3')
        subprocess.run([python_executable, "-m", "pip", "install", shlex_quote(package)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    else:

        python_executable = 'python3'
        subprocess.run([python_executable, "-m", "pip", "install", shlex_quote(package)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

if platform.system()=='Darwin':
    # Define the path to the directory
    directory_path = "/Applications/QGIS.app/Contents/Resources/python/site-packages/opencv_contrib_python-4.3.0.36-py3.9-macosx-10.13.0-x86_64.egg/"

    # Check if the directory exists
    if os.path.exists(directory_path):
        # Delete the directory and its contents
        shutil.rmtree(directory_path)
        print(f"Directory {directory_path} has been deleted.")
    else:
        print(f"Directory {directory_path} does not exist.")

#QMessageBox.information(None, 'ok', str(result.stdout) + '-' + str(result.stderr))

installed_packages_or = {pkg.metadata['Name'] + '==' + pkg.version for pkg in distributions()}

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')

with open(requirements_path, 'r') as f:
    required_packages = set(line.strip() for line in f)

installed_packages = installed_packages_or

missing_packages = required_packages - installed_packages

if missing_packages:

    show_install_dialog(list(missing_packages))
else:
    print("All required packages are already installed.")
    s.setValue('pyArchInit/dependenciesInstalled', True)






if not Pyarchinit_OS_Utility.checkgraphvizinstallation() and s.value('pyArchInit/graphvizBinPath'):
    os.environ['PATH'] += os.pathsep + os.path.normpath(s.value('pyArchInit/graphvizBinPath'))

if not Pyarchinit_OS_Utility.checkpostgresinstallation() and s.value('pyArchInit/postgresBinPath'):
    os.environ['PATH'] += os.pathsep + os.path.normpath(s.value('pyArchInit/postgresBinPath'))

packages = [
    'postgres',
    'graphviz',
]

for p in packages:

    if p.startswith('postgres'):
        try:
            subprocess.call(['pg_dump', '-V'])
        except Exception as e:
            print(e)
            # except Exception as e:
            # if L=='it':
            #QMessageBox.warning(None, 'Pyarchinit',
                                #"INFO: Sembra che postgres non sia installato sul vostro sistema o che non abbiate impostato il percorso in Pyarchinit config. ",
                                #QMessageBox.Ok | QMessageBox.Cancel)

    if p.startswith('graphviz'):
        try:
            subprocess.call(['dot', '-V'])
        except Exception as e:
            print(e)
            #if L == 'it':
                #QMessageBox.warning(None, 'Pyarchinit',
                                    #"INFO: Sembra che Graphviz non sia installato sul vostro sistema o che non abbiate impostato il percorso in Pyarchinit config. In ogni caso il modulo python di graphviz sarà installato sul vostro sistema, ma la funzionalità di esportazione del matrix dal plugin pyarchinit sarà disabilitata.",
                                    #QMessageBox.Ok | QMessageBox.Cancel)
            #if L == 'de':
                #QMessageBox.warning(None, 'Pyarchinit',
                                    #"INFO: Es scheint, dass Graphviz nicht auf Ihrem System installiert ist oder dass Sie den Pfad in der Pyarchinit-Konfiguration nicht festgelegt haben. Wie auch immer, das Graphviz-Python-Modul wird auf Ihrem System installiert sein, aber die Exportmatrix-Funktionalität aus dem Pyarchinit-Plugin wird deaktiviert sein.",
                                    #QMessageBox.Ok | QMessageBox.Cancel)

            #else:
                #QMessageBox.warning(None, 'Pyarchinit',
                                    #"INFO: It seems that Graphviz is not installed on your system or you don't have set the path in Pyarchinit config. Anyway the graphviz python module will be installed on your system, but the export matrix functionality from pyarchinit plugin will be disabled.",
                                    #QMessageBox.Ok | QMessageBox.Cancel)

if platform.system() == "Darwin":
    location = os.path.expanduser("~/Library/Fonts")

    if not path.exists(location + '/cambria.ttc'):

        QMessageBox.warning(None, 'Pyarchinit',
                            "INFO: Il font Cambria sembra non essere installato. per installarlo clicca Ok\n e poi doppio click su cambria.*\Dopo ricarica il plugin",
                            QMessageBox.Ok)

        if QMessageBox.Ok:
            HOME = os.environ['PYARCHINIT_HOME']
            path = '{}{}{}'.format(HOME, os.sep, "bin")

            subprocess.Popen(["open", path])



def classFactory(iface):

    from .pyarchinitPlugin import PyArchInitPlugin
    return PyArchInitPlugin(iface)
