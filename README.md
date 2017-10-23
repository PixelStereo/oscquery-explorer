# OSCQuery Explorer
Standalone application for exploring oscquery devices

# Quickstart
    brew install python3
    pip3 install pyqt5 zeroconf
    cd src
    python3 main.py
    
# Todo
* add pyossia dependancy (waiting for pypi pyossia release)
* add pyinstaller script to release standalone applications

#### v0
* choose one device from a menu, remove the menu and build the remote
* add parameter inspecor (show / hide)
* focus on remotes UI
* make different kind of remotes, view
* add presets for the whole device

#### v1
* Add a checkbox for each parameter in the tree view list (Default = True).
* Build only for checked parameters (If a box is unchecked, delete the view)
* Save view files to remember checkview

#### v2
* Drag and Drop any parameters from the tree view to build your custom remote, mixing devices and protocols
* add mappings for every parameter. Inspector a-la qlab en bas pour inspecter chaque mapping
