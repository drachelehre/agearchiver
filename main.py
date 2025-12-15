import sys
import zipfile
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                            QFileDialog, QMessageBox, QGridLayout)


def archive_files(folder, days, parent):
    cutoff_date = datetime.now() - timedelta(days=days)
    archived = 0

    archive_path, _ = QFileDialog.getSaveFileName(
        parent,
        "Save Archive",
        "",
        "Zip Files (*.zip)"
    )

    if not archive_path:
        return

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                mtime = datetime.fromtimestamp(os.path.getmtime(full_path))

                if mtime < cutoff_date:
                    arcname = os.path.relpath(full_path, folder)
                    zf.write(full_path, arcname)
                    archived += 1
    QMessageBox.information(
        parent,
        "Done",
        f"Archived {archived} files older than {days} days"
    )
def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Age Archiver")

    layout = QGridLayout(window)

    folder_label = QLabel("Select folder")
    folder_edit = QLineEdit()
    browse_button = QPushButton("Browse...")

    days_label = QLabel("Archive files older than (days):")
    days_edit = QLineEdit()

    archive_button = QPushButton("Create archive")

    layout.addWidget(folder_label, 0, 0)
    layout.addWidget(folder_edit, 0, 1)
    layout.addWidget(browse_button, 0, 2)

    layout.addWidget(days_label, 1, 0)
    layout.addWidget(days_edit, 1, 1)

    layout.addWidget(archive_button, 2, 0)

    def browse():
        folder = QFileDialog.getExistingDirectory(window, "Select folder")
        if folder:
            folder_edit.setText(folder)

    def archive():
        folder = folder_edit.text().strip()
        days_text = days_edit.text().strip()

        if not folder or not days_text.isdigit():
            QMessageBox.critical(
                window,
                "Error",
                "Please input valid folder path or number of days"
            )

        archive_files(folder, int(days_text), window)

    browse_button.clicked.connect(browse)
    archive_button.clicked.connect(archive)

    window.show()
    sys.exit(app.exec())



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


