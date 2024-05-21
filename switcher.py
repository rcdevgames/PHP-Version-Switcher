import os
import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QMessageBox

CONFIG_FILE = 'php_version_config.json'

def get_php_versions(directory):
    # List all directories starting with 'php' in the given directory
    versions = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) and name.startswith('php')]
    return versions

def load_active_version():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('active_version')
    return None

def save_active_version(version):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'active_version': version}, f)

def switch_php_version(selected_version):
    global active_version

    php_base_path = r"C:\php"
    current_php_path = os.path.join(php_base_path, "php")
    new_php_path = os.path.join(php_base_path, selected_version)

    # Check if the selected version is already the active one
    if os.path.exists(current_php_path) and os.path.samefile(current_php_path, new_php_path):
        QMessageBox.information(None, "Info", f"PHP {selected_version} is already active")
        return

    try:
        # Rename the current 'php' folder to its original version name
        if active_version and os.path.exists(current_php_path):
            active_version_path = os.path.join(php_base_path, active_version)
            os.rename(current_php_path, active_version_path)

        # Rename the selected version folder to 'php'
        os.rename(new_php_path, current_php_path)
        active_version = selected_version  # Update the active version
        save_active_version(active_version)  # Save the active version to the config file
        QMessageBox.information(None, "Success", f"Switched to PHP {selected_version}")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to switch PHP version: {str(e)}")

class PHPVersionSwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global active_version

        self.setWindowTitle("PHP Version Switcher")
        self.setGeometry(100, 100, 300, 100)
        layout = QVBoxLayout()

        # Create a label
        label = QLabel("Select PHP Version:")
        layout.addWidget(label)

        # Get the list of PHP versions
        php_base_path = r"C:\php"
        self.php_versions = get_php_versions(php_base_path)

        # Load the active version from the config file
        active_version = load_active_version()

        # Create a dropdown menu
        self.version_combo = QComboBox(self)
        self.version_combo.addItem("Select a version")
        self.version_combo.addItems(self.php_versions)
        self.version_combo.currentIndexChanged.connect(self.on_dropdown_change)
        layout.addWidget(self.version_combo)

        self.setLayout(layout)

    def on_dropdown_change(self):
        selected_version = self.version_combo.currentText()
        if selected_version != "Select a version":
            switch_php_version(selected_version)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PHPVersionSwitcher()
    ex.show()
    sys.exit(app.exec_())
