#--------------------------------------------------------------------------------------------------------------------------
#  *                                                      INFO
#    
#    Este archivo se encarga de manejar las solicitudes relacionadas con la funcionalidad de contacto.
#    
# 
#--------------------------------------------------------------------------------------------------------------------------


# src/controllers/contactoController.py
from flask import render_template, request, flash
from src.controllers.baseController import BaseController
from src.models.contactoModel import ContactoModel
from src.entities.contactoEntity import ContactoEntity
from email.mime.text import MIMEText
import smtplib

class ContactoController(BaseController):
    def __init__(self, app):
        prefix = '/contacto'
        super().__init__(app, prefix)

        self.app.route('/contacto', methods=['GET', 'POST'])(self.contacto)

    def send_email(self, nombre, email, mensaje):
        try:
            smtp_server = 'sandbox.smtp.mailtrap.io'
            smtp_port = 587
            smtp_username = 'd7c58f9278522e'
            smtp_password = 'f3d2c0db06c990'

            msg = MIMEText(f'Nombre: {nombre}\nEmail: {email}\nMensaje: {mensaje}')
            msg['Subject'] = 'Nuevo mensaje del formulario de contacto'
            msg['From'] = 'Contactame@dulces.promesas.com'
            msg['To'] = 'MailTrap@inbox.mailtrap.io'

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            server.quit()

            return True
        except Exception as e:
            print(f'Error al enviar el correo: {str(e)}')
            return False

    def contacto(self):
        try:
            if request.method == 'POST':
                nombre = request.form['nombre']
                email = request.form['email']
                mensaje = request.form['mensaje']

                # Crear una instancia de ContactoEntity
                contacto_entity = ContactoEntity(nombre=nombre, email=email, mensaje=mensaje)

                # Usar ContactoModel para insertar en la base de datos
                if ContactoModel.insert_contacto(contacto_entity):
                    # Enviar correo
                    if self.send_email(nombre, email, mensaje):
                        return 'Correo enviado y datos insertados correctamente'
                    else:
                        flash("Error al enviar correo. Intenta de nuevo.", "error")
                        return render_template('contacto.html')

        except Exception as error:
            print(f'Error: {str(error)}')
            flash(f'Error: {str(error)}', 'error')
            return render_template('contacto.html'), 500

        return render_template('contacto.html')
