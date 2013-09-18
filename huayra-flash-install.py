#!/usr/bin/env python
# coding: UTF-8
import pygtk
pygtk.require('2.0')
import gtk
import subprocess

notif = gtk.Label("""
Esta aplicación va a instalar Adobe® Flash Player.
Adobe® Flash Player no es Software Libre.
Queda bajo su responsabilidad el instalar esta aplicación.

Para más información, consulte en adobe.com

Al instalar, se le va a solicitar la contraseña.
La aplicación tardará entre 1 a 10 minutos en instalarse. Por favor, sea paciente.
        """)
 
class FlashPlayerInstaller:
  def __init__(self):
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.set_title("Instalar Flash Player")
    self.window.set_border_width(8)
    self.window.set_size_request(640, 250)
    self.window.connect("delete_event", self.destroy_window)

    # boxes
    vbox = gtk.VBox(False, 5)
    hbox = gtk.HBox(True, 3)

    valign1 = gtk.Alignment(0, 1, 0, 0)
    vbox.pack_start(valign1)

    close = gtk.Button("Cancelar")
    close.connect("clicked", self.destroy_window)
    ok = gtk.Button("Instalar")
    ok.connect("clicked", self.init_install)
    ok.set_size_request(70, 30)

    hbox.add(close)
    hbox.add(ok)

    halign = gtk.Alignment(1, 0, 0, 0)
    halign.add(hbox)

    vbox.pack_start(notif, False, False, False)
    vbox.pack_start(halign, False, False, 3)

    self.window.add(vbox)
    



    self.window.show_all()

  def main(self):
    gtk.main()

  def destroy_window(self, widget=None, event=None, data=None):
    gtk.main_quit()
    return False # devolver 0

  def show_error(self, text):
    md = gtk.MessageDialog(self.window, 
        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
        gtk.BUTTONS_CLOSE, text)
    md.run()
    md.destroy()

  def show_success(self, text):
    md = gtk.MessageDialog(self.window, 
        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
        gtk.BUTTONS_CLOSE, text)
    md.run()
    md.destroy()

  def init_install(self, widget, data=None):
    notif.set_text("Instalando...") # marcar como "instalando"
    command = 'gksu "update-flashplugin-nonfree --install --verbose"'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while p.poll() == None:
      pass # esperar a que termine
    if p.returncode == 0: # todo bien
      self.show_success('Flash Player se ha instalado correctamente.')
      self.destroy_window()
    else:
      self.show_error("Ocurrió un error instalando Flash Player.\nPor favor, revisá que estés conectado a internet.")
      self.destroy_window()



if __name__ == "__main__":
  fpi = FlashPlayerInstaller()
  fpi.main()