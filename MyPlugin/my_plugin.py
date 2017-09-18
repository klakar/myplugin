# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MyPlugin
                                 A QGIS plugin
 Detta är mitt plugin
                              -------------------
        begin                : 2017-09-17
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Klas Karlsson
        email                : klaskarlsson@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from my_plugin_dialog import MyPluginDialog
import os.path
# Importera kod för lagerhantering
from qgis.core import QgsMapLayer, QgsMapLayerRegistry
# Importera kod för att hantera teckenkodstabeller
import sys
reload(sys)

class MyPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MyPlugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&MyPlugin')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MyPlugin')
        self.toolbar.setObjectName(u'MyPlugin')
        
    def create_vector_combo(self):
    	self.dlg.combo_layer.clear()								# Rensa comboboxen från tidigare värden
    	#self.dlg.combo_attribute.clear()							# Rensa comboboxen från tidigare värden
    	layers = self.iface.legendInterface().layers()   	# Skapa ett objekt för alla lager i projektet
    	for layer in layers:											# För varje lager i listan...
    		layerType = layer.type()								# Spara typ av lager i en variabel
    		if layerType == QgsMapLayer.VectorLayer:			# Kontrollera om det är av typen "vektor"
    			self.dlg.combo_layer.addItem(layer.name())	# Lägg till lagernamnet till combolistan
    	
    def create_attribute_combo(self):
    	vector_layer = self.dlg.combo_layer.currentText()												# Hämta valt lagernamn från combo_layer
    	#QgsMessageLog.logMessage("Fungerar", 'MyPlugin', QgsMessageLog.INFO)
    	self.dlg.combo_attribute.clear()																		# Rensa comboboxen från tidigare värden
    	layer_actual = QgsMapLayerRegistry.instance().mapLayersByName(vector_layer)			# Hämta lagerobjektet från lagernamnet
    	layer_attributes = [attribute.name() for attribute in layer_actual[0].fields()]		# Skapa lista med attributnamnen i lagret
    	self.dlg.combo_attribute.addItems(layer_attributes)											# Lägg till hela listan i comboboxen
    	
    def create_text_list(self):
    	vector_layer = self.dlg.combo_layer.currentText()										# Hämta valt lagernamn till en variable
    	layer_actual = QgsMapLayerRegistry.instance().mapLayersByName(vector_layer)	# Hämta lagerobjektet från lagernamnet
    	attribute_name = self.dlg.combo_attribute.currentText()								# Hämta texten från attribut combon
    	idx = layer_actual[0].fields().fieldNameIndex(attribute_name)						# Hämta attribut index baserat på valt namn
    	values = layer_actual[0].uniqueValues(idx)												# Skapa en lista med unika värden från fältet med index från förra raden
    	if (self.dlg.check_list.isChecked()):														# Om checkboxen är markerad
    		sep = ", "																						# Använd kommatecken
    	else:																									# Annars...
    		sep = "\n"																						# Använd ny-rad
    	text_out = ""																						# Rensa textvariabeln
    	for value in values:																				# För varje unikt fältvärde...
    		value = str(value)																			# Gör om detta till text (även om det redan är det)
    		text_out += value.encode('latin1') + sep												# Koda värdet till Latin1 och lägg till vald separator baserad på checkbox
    	self.dlg.text_out.setPlainText(text_out)													# När hela listan är klar skriv texten till textrutan i dialogen
    	

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MyPlugin', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = MyPluginDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/MyPlugin/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'My Plugin'),
            callback=self.run,
            parent=self.iface.mainWindow())



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MyPlugin'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        sys.setdefaultencoding('utf-8')
        	
        # show the dialog
        self.dlg.show()
        
        # Läs in alla vektorlager
        self.create_vector_combo()
        
        # Koppla dialogens element till funktioner
        self.dlg.combo_layer.currentIndexChanged.connect(self.create_attribute_combo)
        self.dlg.combo_attribute.currentIndexChanged.connect(self.create_text_list)

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
        	pass
