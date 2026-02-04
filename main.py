import sys
import zipfile
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                            QFileDialog, QMessageBox, QGridLayout, QCalendarWidget, QProgressDialog)
from PyQt6.QtCore import (Qt)


def archive_files(folder, days, parent):
    """
    Searches a folder for files past a threshold (in days)
    and archives them into a zip file placed in the same directory.
    Update: Includes calendar and progress bar.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    archived = 0

    # Parent directory of the selected folder
    parent_dir = os.path.dirname(folder.rstrip(os.sep))
    folder_name = os.path.basename(folder.rstrip(os.sep))

    # Archive name (example: MyFolder_archive_2026-02-03.zip)
    archive_name = f"{folder_name}_archive_{datetime.now():%Y-%m-%d}.zip"
    archive_path = os.path.join(parent_dir, archive_name)

    total_files = 0
    for _, _, files in os.walk(folder):
        total_files += 1

    if total_files == 0:
        QMessageBox.information(parent, "Nothing to do. No files in target folder.")
        return

    progress = QProgressDialog(
        "Archiving in progress...",
        "Cancel",
        0,
        total_files,
        parent
    )

    progress.setWindowTitle("Archiving files")
    progress.setWindowModality(Qt.WindowModality.WindowModal)
    progress.setMinimumDuration(0)
    progress.show()

    processed = 0
    try:
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(folder):
                for file in files:
                    if progress.wasCanceled():
                        raise Exception("Cancelled")

                    full_path = os.path.join(root, file)
                    mtime = datetime.fromtimestamp(os.path.getmtime(full_path))

                    if mtime < cutoff_date:
                        arcname = os.path.relpath(full_path, folder)
                        zf.write(full_path, arcname)
                        archived += 1
                        os.remove(full_path)

                    processed += 1
                    progress.setValue(processed)

        progress.close()

        QMessageBox.information(
            parent,
            "Done",
            f"Archived {archived} files\n\nArchive created at:\n{archive_path}"
        )
    except Exception:
        progress.close()
        if os.path.exists(archive_path):
            os.remove(archive_path)
        QMessageBox.warning(parent, "Canceled", "Archiving canceled.")


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Age Archiver")

    layout = QGridLayout(window)

    folder_label = QLabel("Select folder")
    folder_edit = QLineEdit()
    browse_button = QPushButton("Browse...")

    days_label = QLabel("Archive files older than (date):")
    day_selected_label = QLabel("No date selected")
    calendar = QCalendarWidget()
    calendar.setGridVisible(True)

    def on_date_selected():
        selected_date = calendar.selectedDate()
        day_selected_label.setText(f"{selected_date.toString("MM/dd/yyyy")}")

    calendar.selectionChanged.connect(on_date_selected)

    archive_button = QPushButton("Create archive")

    layout.addWidget(folder_label, 0, 0)
    layout.addWidget(folder_edit, 0, 1)
    layout.addWidget(browse_button, 0, 2)

    layout.addWidget(days_label, 1, 0)
    layout.addWidget(calendar, 1, 1)
    layout.addWidget(day_selected_label, 2, 0)

    layout.addWidget(archive_button, 3, 0)

    def browse():
        """
        opens a dialogue window that allows for searching for target folder
        :return: None
        """
        folder = QFileDialog.getExistingDirectory(window, "Select folder")
        if folder:
            folder_edit.setText(folder)

    def archive():
        """
        Takes input from text boxes in main window and archives folders based off of them
        :return: None
        """
        folder = folder_edit.text().strip()
        selected_qdate = calendar.selectedDate()

        if not folder:
            QMessageBox.critical(window, "Error", "Please select a folder")
            return

        selected_date = selected_qdate.toPyDate()
        today = datetime.today().date()
        days = (today - selected_date).days

        if days < 0:
            QMessageBox.critical(window, "Error", "Selected date is in the future")
            return

        archive_files(folder, days, window)

    browse_button.clicked.connect(browse)
    archive_button.clicked.connect(archive)

    window.show()
    sys.exit(app.exec())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


