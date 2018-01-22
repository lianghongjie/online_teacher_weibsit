# -*- coding: utf-8 -*-
from BQt import QtGui, QtWidgets, QtCore
import os
import sys
from rename_dialog import RenameDialog
from core import AttachmentParser, BatchParser
from constances import LINK_PATH, COPY_PATH
from bfx.data.prod.shotside import get_approved_shows
import core
import shotgun_api3
from constances import SG_CONNECT, SG_CONNECT_2
from icons import FILE_ICON, PASSED, FAILED
from rename_check import RenameCheck
from check_dialog import CheckItemDialog
from bfx.ui import get_icon
import shutil
from custom_widget import CustomTablewidget, CustomValidator, OverwriteDialog


SG = shotgun_api3.Shotgun(**SG_CONNECT)
SG_2 = shotgun_api3.Shotgun(**SG_CONNECT_2)
SG_DATA = 101


class Model(object):
    def __init__(self):
        self.mode_model = QtCore.QStringListModel(["Shot", "Asset"])
        self.upload_type = QtCore.QStringListModel(["Attachment", "Thumbnail", "Reference_qt"])
        self.show_model = QtGui.QStandardItemModel()
        self.path_model = QtWidgets.QDirModel()

        shows = get_approved_shows()
        for show_item in shows.items():
            if show_item[1] in frozenset(['production', 'production2']):
                item = QtGui.QStandardItem(show_item[0])
                item.setData(show_item[1], SG_DATA)
                self.show_model.appendRow(item)
        self.tree_model = QtWidgets.QFileSystemModel()
        self.tree_model.setRootPath("/")
        self.none_tree = QtWidgets.QFileSystemModel()


class MainWindow(QtWidgets.QWidget):
    def __init__(self, model):
        QtWidgets.QWidget.__init__(self)
        self.sg = None
        self.model = model
        self.copy_path = COPY_PATH  # ignore BE001
        self.setWindowTitle("Batch Uploader")
        self.resize(700, 800)
        screen_size = QtWidgets.QDesktopWidget().geometry()
        self.move((screen_size.width() - self.width()) / 2, (screen_size.height() - self.height()) / 2)
        self.setAcceptDrops(True)
        self.element_widget()

    def element_widget(self):
        show_label = QtWidgets.QLabel("Show")
        self.path_label = QtWidgets.QLabel("Reference Path")
        mode_label = QtWidgets.QLabel("Mode")
        upload_type = QtWidgets.QLabel("Type")

        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.model.none_tree)
        self.tree_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tree_view.setColumnWidth(0, 450)
        self.tree_view.setColumnWidth(1, 80)
        self.tree_view.setColumnWidth(2, 50)
        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)
        rename_label = QtWidgets.QLabel("Selected File  ")
        rename_label.setFont(QtGui.QFont('Timer', 13))
        delete_action = QtWidgets.QAction('Delete row', self)
        delete_action.triggered.connect(self.delete_row)
        file_name_item = QtWidgets.QAction('Create alias name', self)
        file_name_item.triggered.connect(lambda: self.rename_dialog(type='alias_name'))
        alias_name_item = QtWidgets.QAction('Modify alias name', self)
        alias_name_item.triggered.connect(lambda: self.rename_dialog(type='modify_alias_name'))
        self.file_name_menu = QtWidgets.QMenu('Create alias name', self)
        self.file_name_menu.addAction(delete_action)
        self.file_name_menu.addAction(file_name_item)
        self.alias_name_menu = QtWidgets.QMenu('Modify alias name', self)
        self.alias_name_menu.addAction(delete_action)
        self.alias_name_menu.addAction(alias_name_item)

        self.rename_table = CustomTablewidget()
        self.rename_table.customDataChanged.connect(self.rename_command)
        self.rename_table.customContextMenuRequested.connect(self.set_item_menu)

        self.uploader_button = QtWidgets.QPushButton("Upload")
        self.uploader_button.setFont(QtGui.QFont('Timer', 13))
        self.uploader_button.setMinimumHeight(40)
        self.uploader_button.setEnabled(False)
        self.uploader_button.clicked.connect(self.upload_button_command)
        self.copy_file_path_label = QtWidgets.QLabel("Copy reference to:")
        self.copy_file_path_edit = QtWidgets.QLineEdit()
        self.copy_file_path_edit.setText("")
        self.show_line_combox = QtWidgets.QComboBox()
        self.show_line_combox.setModel(self.model.show_model)
        self.show_line_combox.currentIndexChanged.connect(self.show_line_command)
        self.show_line_combox.setFixedWidth(90)
        self.mode_combo_box = QtWidgets.QComboBox()
        self.mode_combo_box.setModel(self.model.mode_model)
        self.mode_combo_box.currentIndexChanged.connect(self.mode_combo_box_command)
        self.path_edit = QtWidgets.QLineEdit()
        self.path_completer = QtWidgets.QCompleter()
        self.path_completer.setModel(self.model.path_model)
        self.path_edit.setCompleter(self.path_completer)
        self.path_edit.returnPressed.connect(self.path_completion)
        self.path_edit.setFixedWidth(300)
        self.path_edit.textChanged.connect(self.set_root_path)

        self.file_select = QtWidgets.QToolButton()
        self.file_select.setIcon(QtGui.QIcon(FILE_ICON))
        self.file_select.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.file_select.clicked.connect(self.open_file_path)
        self.upload_type = QtWidgets.QComboBox()
        self.upload_type.setFixedWidth(95)
        self.upload_type.setModel(self.model.upload_type)
        self.upload_type.currentIndexChanged.connect(self.upload_type_command)

        show_mode_hbox = QtWidgets.QHBoxLayout()
        show_hbox = QtWidgets.QHBoxLayout()
        show_hbox.addWidget(show_label)
        show_hbox.addWidget(self.show_line_combox)
        show_hbox.addStretch(1)
        mode_hbox = QtWidgets.QHBoxLayout()
        mode_hbox.addWidget(mode_label)
        mode_hbox.addWidget(self.mode_combo_box)
        mode_hbox.addStretch(1)
        type_hbox = QtWidgets.QHBoxLayout()
        type_hbox.addWidget(upload_type)
        type_hbox.addWidget(self.upload_type)
        type_hbox.addStretch(1)
        show_mode_hbox.addLayout(show_hbox)
        show_mode_hbox.addLayout(mode_hbox)
        show_mode_hbox.addLayout(type_hbox)

        path_file_select_hbox = QtWidgets.QHBoxLayout()
        path_file_select_hbox.addWidget(self.path_label)
        path_file_select_hbox.addWidget(self.path_edit)
        path_file_select_hbox.addWidget(self.file_select)
        show_mode_hbox.addLayout(path_file_select_hbox)

        copy_path_hbox = QtWidgets.QHBoxLayout()
        copy_path_hbox.addWidget(self.copy_file_path_label)
        copy_path_hbox.addWidget(self.copy_file_path_edit)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(show_mode_hbox)
        vbox.addSpacing(10)
        vbox.addLayout(copy_path_hbox)
        vbox.addSpacing(10)
        vbox.addWidget(self.tree_view)
        vbox.addWidget(rename_label, 0, QtCore.Qt.AlignCenter)
        vbox.addWidget(self.rename_table)
        self.attachment_widget = QtWidgets.QWidget()
        attachment_vbox = QtWidgets.QVBoxLayout()
        self.attachment_widget.setLayout(attachment_vbox)
        self.attachment_widget.setVisible(True)
        vbox.addWidget(self.attachment_widget)
        vbox.addWidget(self.uploader_button)
        self.setLayout(vbox)

        self.show_line_combox.currentIndexChanged.emit(0)

    def set_item_menu(self, pos):
        item = self.rename_table.itemAt(pos)
        if item and item.column() == 1:
            self.file_name_menu.exec_(self.rename_table.mapToGlobal(pos))
        elif item and item.column() == 3:
            self.alias_name_menu.exec_(self.rename_table.mapToGlobal(pos))

    def set_copy_edit_show(self, show=True):
        self.copy_file_path_edit.setVisible(show)
        self.copy_file_path_label.setVisible(show)

    def set_root_path(self):
        path = self.path_edit.text()
        if os.path.exists(str(path)):
            self.tree_view.setModel(self.model.tree_model)
            self.tree_view.setRootIndex(self.model.tree_model.index(path))
        else:
            self.tree_view.setModel(self.model.none_tree)

    def dragEnterEvent(self, drag_event):  # ignore N802
        if drag_event.mimeData().hasUrls():
            drag_event.accept()

    def dropEvent(self, drop_event):  # ignore N802
        if drop_event.mimeData().hasUrls():
            drop_urls = drop_event.mimeData().urls()
            for url in drop_urls:
                local_path = url.toLocalFile()
                if os.path.isfile(str(local_path)):
                    file_name = str(local_path).rsplit(os.path.sep, 1)[1]
                    self.add_item(file_name, local_path)
                elif os.path.isdir(str(local_path)):
                    for file_name in os.listdir(str(local_path)):
                        file_path = os.path.join(str(local_path), file_name)
                        if os.path.isfile(file_path):
                            self.add_item(file_name, file_path)

    def add_item(self, file_name, local_path):
        count = self.rename_table.rowCount()
        self.rename_table.insertRow(count)
        item = QtWidgets.QTableWidgetItem(file_name)
        item.setToolTip('source name')
        self.rename_table.setItem(count, 1, item)
        rename_item = QtWidgets.QTableWidgetItem('')
        rename_item.setToolTip('alias name')
        self.rename_table.setItem(count, 3, rename_item)
        self.rename_table.setItem(count, 2, QtWidgets.QTableWidgetItem(local_path))
        self.add_button(count, file_name)

    def add_button(self, index, file_name):
        if self.check_file_name(file_name):
            color = "green"
            icon = PASSED
        else:
            color = 'red'
            icon = FAILED
        check_button = QtWidgets.QPushButton()
        check_button.setFlat(True)
        check_button.setIcon(get_icon(icon, color))
        check_button.clicked.connect(self.check_state)
        self.rename_table.setCellWidget(index, 0, check_button)

    def rename_command(self, row, column, item):
        if item:
            file_name = item.text()
            if not file_name:
                file_name = self.rename_table.item(row, 1).text()
            self.add_button(row, str(file_name))

    def rename_dialog(self, type):
        rename_list = []
        for index in self.rename_table.selectedIndexes():
            if index.column() == 1:
                rename_list.append(str(self.rename_table.item(index.row(), 1).text()))
            else:
                context = self.rename_table.item(index.row(), 3)
                if context:
                    rename_list.append(str(context.text()))
        self.rename = RenameDialog(rename_list, type, parent=self)
        rename_list = self.rename.new_filed
        if rename_list:
            count = 0
            for index in self.rename_table.selectedIndexes():
                if rename_list[count]:
                    item = QtWidgets.QTableWidgetItem(rename_list[count])
                    item.setToolTip('alias name')
                    self.rename_table.setItem(index.row(), 3, item)
                count += 1

    def check_state(self):
        point = self.sender().pos()
        index = self.rename_table.indexAt(point).row()
        show_name = self.show_line_combox.currentText()
        upload_type = str(self.upload_type.currentText()).lower()
        mode = str(self.mode_combo_box.currentText())
        file_name = self.rename_table.item(index, 3).text()
        if file_name:
            try:
                file_name = str(file_name.text())
            except AttributeError:
                file_name = str(file_name)
        else:
            file_name = str(self.rename_table.item(index, 1).text())
        self.check_dialog = CheckItemDialog(mode=mode, show_name=show_name, file_name=file_name,
                                            upload_type=upload_type)

    def delete_row(self):
        indexs = self.rename_table.selectedIndexes()
        num = []
        if len(indexs) >= 0:
            for index in indexs: num.append(index.row())
            num.sort(reverse=True)
            for i in num: self.rename_table.removeRow(i)

    def keyPressEvent(self, delete):  # ignore N802
        if delete.key() == QtCore.Qt.Key_Delete: self.delete_row()

    def link_file(self, file_path, link_name, execute):
        root_link_path = LINK_PATH.format(str(self.show_line_combox.currentText()),
                                          str(self.upload_type.currentText()).lower())
        if not os.path.exists(root_link_path): os.makedirs(root_link_path)
        link_path = os.path.join(root_link_path, link_name)
        if execute:
            try:
                os.symlink(file_path, link_path)
            except OSError:
                os.remove(link_path)
                os.symlink(file_path, link_path)
        return link_path

    def check_file_name(self, file_name):
        upload_type = str(self.upload_type.currentText()).lower()
        show_name = self.show_line_combox.currentText()
        mode = str(self.mode_combo_box.currentText())
        check = RenameCheck(mode, upload_type, file_name, show_name).check_result
        return check

    def clear_table_data(self):
        for index in xrange(self.rename_table.rowCount()):
            self.rename_table.removeRow(0)

    def mode_combo_box_command(self):
        self.clear_table_data()

    def upload_type_command(self):
        upload_type = str(self.upload_type.currentText()).lower()
        self.copy_file_path_label.setText("Copy {0} to:".format(upload_type))
        self.path_label.setText("{0} Path:".format(upload_type))
        self.clear_table_data()
        if self.upload_type.currentIndex() == 0:
            self.set_copy_edit_show(True)
        else:
            self.set_copy_edit_show(False)

    def path_completion(self):
        self.path_edit.setText(self.path_completer.currentCompletion())

    def show_line_command(self, data):
        self.upload_type.setCurrentIndex(0)
        shotgun_type = self.show_line_combox.itemData(data, SG_DATA).toPyObject()
        if shotgun_type == 'production':
            self.sg = SG
        else:
            self.sg = SG_2
        self.clear_table_data()
        self.uploader_button.setEnabled(True)
        show_name = self.show_line_combox.currentText()
        self.copy_file_path_edit.setValidator(CustomValidator(30))
        self.copy_file_path_edit.setText(
            ("/show/{0}" + self.copy_path + str(self.upload_type.currentText()).lower()).
                format(show_name))
        length = len(self.copy_file_path_edit.text())
        self.copy_file_path_edit.setValidator(CustomValidator(length))

    def open_file_path(self):
        self.path_edit.clear()
        path = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory', options=QtWidgets.
                                                              QFileDialog.DontUseNativeDialog))
        self.path_edit.setText(path)

    def upload_button_command(self):
        self.override = None
        self.temp_override = None
        upload_type = str(self.upload_type.currentText())
        for index in xrange(self.rename_table.rowCount()):
            link_name = self.rename_table.item(index, 3)
            if link_name and link_name.text() != '':
                link_name = str(link_name.text())
                src_path = str(self.rename_table.item(index, 2).text())
                # if self.check_file_name(link_name):
                path = self.link_file(src_path, link_name, execute=False)
                file_name = link_name
            else:
                file_name = str(self.rename_table.item(index, 1).text())
                path = str(self.rename_table.item(index, 2).text())
            if self.check_file_name(file_name):
                entity_type = str(self.mode_combo_box.currentText())
                show_name = str(self.show_line_combox.currentText())
                if upload_type == "Attachment":
                    parser = AttachmentParser(file_name=file_name, path=path, show_name=show_name,
                                              mode=entity_type, sg=self.sg)
                else:
                    parser_type = str(self.upload_type.currentText())
                    parser = BatchParser(file_name=file_name, path=path, show_name=show_name, mode=entity_type,
                                         parser_type=parser_type, sg=self.sg)
                exist_file = parser.existed_file
                parser_parmater = parser.batch_upload
                if exist_file:
                    if self.override is None:
                        self.show_override_dialog = OverwriteDialog(exist_file)
                        if self.show_override_dialog.override is True:
                            self.override = True
                        elif self.show_override_dialog.override is False:
                            self.override = False
                        else:
                            if self.show_override_dialog.temp_override is True:
                                self.temp_override = True
                            elif self.show_override_dialog.temp_override is False:
                                self.temp_override = False
                    if self.override is True:
                        self.link_file(str(self.rename_table.item(index, 2).text()), file_name, execute=True)
                        parser_parmater = parser.existed_upload
                    elif self.override is None and self.temp_override is True:
                        self.link_file(str(self.rename_table.item(index, 2).text()), file_name, execute=True)
                        parser_parmater = parser.existed_upload
                else:
                    self.link_file(str(self.rename_table.item(index, 2).text()), file_name, execute=True)
                print "@upload@:", parser_parmater
                if parser_parmater:
                    entity_id = parser_parmater["entity_id"]
                    file_path = parser_parmater["file_path"]
                    if upload_type == "Attachment":
                        description = parser_parmater["description"]
                        entity = parser_parmater["entity"]
                        core.upload_attachments(description, entity, entity_type, entity_id, file_path, self.sg)
                        if self.override is True or self.temp_override is True or \
                                (self.override is None and self.temp_override is None):
                            self.copy_file(file_path)
                    else:
                        entity_type = parser_parmater["entity_type"]
                        core.upload_thumbnail_reference_qt(entity_type, entity_id, file_path, parser_type, self.sg)
        if self.rename_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "Information", "Finished!")
            self.clear_table_data()

    def copy_file(self, file_path):
        drt_path = str(self.copy_file_path_edit.text())
        try:
            os.makedirs(drt_path)
        except OSError:
            pass
        shutil.copy(file_path, drt_path)


def main(args):
    app = QtWidgets.QApplication(args)
    model = Model()
    window = MainWindow(model)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    w = MainWindow(model)
    w.show()
    sys.exit(app.exec_())
