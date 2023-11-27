
// Constantes que necesitaremos para abrir y cerrar el carrito
const mostrarAside = document.getElementById('mostrarAside');
const cerrar = document.getElementById('cerrar')
const icono = document.getElementById('icono')
const miAside = document.getElementById('miAside');

let intentos = 0

mostrarAside.addEventListener('click', () =>{

    if(intentos <= 1){
        Swal.fire({
            title: 'Bienvenido a tu carrito',
            text: 'Aquí verás los productos que elegiste y podrás personalizarlos',
            icon: 'info',
            confirmButtonText: 'De acuerdo'
          })
        intentos++
        console.log(intentos)
    }

    if (miAside.style.right === '-400px'){
        miAside.style.right = '0'
        icono.style.display = 'none'
        miAside.style.boxShadow = '-5px 0 10px rgba(0, 0, 0, 0.356)'
    } else{
        miAside.style.right = '-400px';
    }
})

cerrar.addEventListener('click', () =>{
    miAside.style.right = '-400px'
    icono.style.display = 'inline'
    miAside.style.boxShadow = 'none'
})


const botones = document.querySelectorAll('.buy')


botones.forEach(boton => {
    let clicks = 0;
    boton.addEventListener('click', () => {
        if (clicks < 1) {
            Swal.fire({
                title: 'ADVERTENCIA',
                text: 'Los productos que decidas comprar se almacenarán en tu carrito',
                icon: 'info',
                confirmButtonText: 'De acuerdo'
            })
            clicks++
        } else if (clicks >= 1) {
            Swal.fire({
                title: 'Agregado Exitosamente',
                text: 'Podrás ver este producto en tu carrito',
                icon: 'success',
                confirmButtonText: 'De acuerdo'
            })

            function agregarCarrito(nombre, precio) {
                const cajaCarrito = document.createElement('div')
                cajaCarrito.classList.add('contSelect')
                cajaCarrito.innerHTML = `
                <div class="titlePedido">
  
                <p id="tituloInsert">${nombre}</p>
  
              </div>
  
              <div class="pedido">
                  <div class="contNumber">
                      <div class="contPrin">
                          <div class="restar cajita"><button class="botMenos" id="menos">-</button></div>
                          <div class="numero cajita"><p id="numerito">1</p></div>
                          <div class="sumar cajita"><button class="botMas" id="mas">+</button></div>
                      </div>
                  </div>
                      
                  <div class="contPrecio">
                      <input value ="S/${precio}.00" class="compra" type="text" readonly>
                  </div>
              </div>
  
              <div class="titleNotas">
                  <p id="notas">Notas para el pedido</p>
              </div>
  
              <div class="notas">
                  <div class="textArea">
                      <textarea id="notitas"></textarea>
                  </div>
                  <div class="eliminar">
                      <p id="eliminarPedido">Eliminar Pedido</p>
                  </div>
              </div>
                `
                miAside.appendChild(cajaCarrito)
            }

            const producto = boton.closest('.pastel');
            const nombreProducto = producto.querySelector('.pastelTitle p').textContent;
            const precioProducto = parseFloat(producto.querySelector('.pastelPrecio p').textContent.replace('S/', ''));

            agregarCarrito(nombreProducto, precioProducto);

            clicks++;
        } else {
            Swal.fire({
                title: 'Ocurrió un error desconocido',
                text: 'Inténtalo denuevo más tarde',
                icon: 'error',
                confirmButtonText: 'De acuerdo'
            })
        }
    })
})