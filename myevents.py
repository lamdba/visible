
from PyQt5.QtCore import pyqtSlot

class E:
    @pyqtSlot()
    def on_button_design_clicked(self):
        self.button_design.hide()
        self.button_test.show()
        self.choose_button(0)

        self.t = 0
        self.label_2.setText(str(0))

        for neuron in self.group.neurons:
            neuron.value = False
        self.scene.update()

        self.d_or_t = 0


    @pyqtSlot()
    def on_button_test_clicked(self):
        self.button_test.hide()
        self.button_design.show()
        self.d_or_t = 1

    @pyqtSlot()
    def on_button_cursor_clicked(self):
        self.choose_button(0)

    @pyqtSlot()
    def on_button_en_clicked(self):
        self.choose_button(1)

    @pyqtSlot()
    def on_button_in_clicked(self):
        self.choose_button(2)

    @pyqtSlot()
    def on_button_connect_clicked(self):
        self.choose_button(3)

    @pyqtSlot()
    def on_button_continue_clicked(self):
        self.button_continue.hide()
        self.button_next.hide()
        self.button_pause.show()

    @pyqtSlot()
    def on_button_pause_clicked(self):
        self.button_pause.hide()
        self.button_continue.show()
        self.button_next.show()

    @pyqtSlot()
    def on_button_next_clicked(self):
        self.group.evo()
        self.scene.update()
        self.t += 1
        self.label_2.setText(str(self.t))


