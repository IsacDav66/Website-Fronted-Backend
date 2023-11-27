const enviar = document.getElementById('enviarForm');
let intentos = 0;

enviar.addEventListener('click', () =>{
    let nombre = document.getElementById('nom').value
    let email = document.getElementById('gmail').value

    if (intentos == 0){

        if(nombre.length < 10 || email.length < 10){
            if(nombre.length < 10){
                Swal.fire({
                    title: 'Nombre Inválido',
                    text: 'El nombre ingresado es muy corto.',
                    icon: 'error',
                    confirmButtonText: 'volver'
                })
            }else if(email.length < 10){
                Swal.fire({
                    title: 'E-mail Inválido',
                    text: 'El Email ingresado es muy corto.',
                    icon: 'error',
                    confirmButtonText: 'volver'
                })
            }
        }else if(nombre.length >= 10 &&  email.length >= 10){
            intentos++
            
            Swal.fire({
                title: 'Enviado Correctamente',
                text: 'Te responderemos a la brevedad.',
                icon: 'success',
                confirmButtonText: 'Okey'
            })
            
            const caja = document.getElementById('avisoID')
            let nuevoParrafo = document.createElement('p')
            nuevoParrafo.classList.add('avisoEnviar')
            nuevoParrafo.textContent = `Hola, ${nombre}, gracias por comunicarte con nosotros, te responderemos a la brevedad al siguiente correo: ${email}.`
            caja.append(nuevoParrafo)
            
            console.log(intentos)
        }

    }else if(intentos >= 1){
        Swal.fire({
            title: 'Mensaje Desestimado',
            text: 'Acabas de enviar un mensaje con anterioridad, debes esperar para enviar otro.',
            icon: 'warning',
            confirmButtonText: 'Okey'
        })

    }

})