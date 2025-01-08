document.addEventListener('DOMContentLoaded', async () => {
  // * Autofocus en el textarea
  document.getElementById('message-input').focus()

  const btnAdjunto = document.querySelector('#btnAdjunto');

  document.addEventListener("visibilitychange", function () {
    // El usuario regresó a la pestaña
    if (document.visibilityState === "visible") scrollBottomChat();
  });

  btnAdjunto.addEventListener('click', async (e) => {
    const { value: file } = await Swal.fire({
      title: 'Selecciona archivo',
      input: 'file',
      inputAttributes: {
        'accept': '.jpg, .jpeg, .png, .gif, .mp4, .avi, .mp3, .ogg, .pdf, .doc, .docx',
        'name': 'file'
      },
      confirmButtonColor: '#0C82C5',
      confirmButtonText: `Enviar <i class='bx bxs-send' style="font-size: .8rem;"></i>`
    });

    if (file) {
      const tiposPermitidos = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'audio/mp3', 'audio/ogg,', 'audio/mpeg', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      let msgError = null;

      if (!tiposPermitidos.includes(file.type)) msgError = 'Tipo de archivo no permitido.';
      
      if (file.size > 5000000) msgError = 'El archivo no puede superar los 5MB';

      if (msgError) return Swal.fire({ icon: 'error', title: msgError });

      const url = `${BOTCHATWEBHOOK_URL}/inMessage`; // Reemplaza con la URL de tu servidor Flask

      try {
        const formData = new FormData();
        formData.append('file', file)
        formData.append('clientId', localStorage.getItem('clientId'));
        const response = await axios.post(url, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        console.log("antes validacion", localStorage.getItem('clientId'));
        await agregarMensaje({ fileData: response.data, remitenteId: localStorage.getItem("clientId"), isPropio: true });
      } catch (error) {
        console.log('Error', error);
        const isPropio = true;
        const chatMessages = document.getElementById("chat-messages");
        const mensajeElemento = document.createElement("div");
        mensajeElemento.className = "chat-message";

        const bubbleElemento = document.createElement("div");
        bubbleElemento.className = `chat-bubble ${isPropio ? 'own' : 'other'}`;

        bubbleElemento.innerHTML = `
          <strong>⚠️ *El documento adjunto no es válido.</strong> <br>
          <i>⚠️ El documento debe ser un archivo .pdf, .xls, .jpg, .png, .doc únicamente y no debe superar los 5 MB.</i>
        `;

        mensajeElemento.appendChild(bubbleElemento);
        chatMessages.appendChild(mensajeElemento);

        setTimeout(() => { scrollBottomChat() }, 1500);
      }
    }
  });

  function hidechatbar() {
    const url = `${BOTCHATWEBHOOK_URL}/validarChat`; // Reemplaza con la URL de tu servidor Flask

    axios
      .post(url, {
        clientId: clientId,
      })
      .then((response) => {
        //console.log("La respuesta es: ",response.data); // Respuesta del servidor Flask
        validar = response.data.trim()
        //console.log("validar:",validar)
        if (validar == "Cerrado") {
          document.getElementById("barraInferior").style.display = "none"
        }
      })
      .catch((error) => {
        console.error(error);
      });
    //console.log("cuando finaliza la funcion es: ",validar)
  }

  // * emojis
  let selectedEmoji = "";

  function handleEmojiSelect(emoji) {
    selectedEmoji = emoji.native;
    const messageInput = document.getElementById("message-input");
    messageInput.value += selectedEmoji;
  }

  const pickerOptionsEmoji = { onEmojiSelect: handleEmojiSelect };
  const pickerEmoji = new EmojiMart.Picker(pickerOptionsEmoji);
  const emojiPicker = document.getElementById("emoji-picker");
  emojiPicker.appendChild(pickerEmoji);
  emojiPicker.style.display = "none";

  // * socket
  const socket = io();

  let clientId;

  // Manejar evento 'cliente-anterior' enviado por el servidor
  socket.on("server_node:cliente-anterior", (previousClientId) => {
    if (previousClientId == null) {
      clientId = socket.id;
    } else {
      clientId = previousClientId;
    }

    if (clientId != null) {
      localStorage.setItem("clientId", clientId);
    } else {
      clientId = socket.id;
      localStorage.setItem("clientId", clientId);
    }
    console.log(clientId);
  });

  // Generar un nuevo ID de cliente
  function generateClientId() {
    const randomId = Math.random().toString(36).substr(2, 8); // Generar un ID aleatorio de 8 caracteres
    return randomId;
  }


  // Manejo del evento 'mensaje' cuando se recibe un mensaje del agente a mi (usuario externo)
  socket.on("server_node:mensaje", (data) => {
    const { isFile, remitenteId } = data;

    isFile
      ? agregarMensaje({ fileData: data.fileData, remitenteId, isPropio: false })
      : agregarMensaje({ mensaje: data.mensaje, remitenteId, isPropio: false });
  });

  // * Formatear el texto
  function formatearTexto(texto) {
    // Expresión regular para detectar enlaces
    const regexEnlace = /(http[s]?:\/\/[^\s]+)/g;
    const regexBold = /\*(.*?)\*/g;
    const regexItalic = /\_(.*?)\_/g;
    let resultado = '';
  
    // Reemplazar enlaces con etiquetas <a> que abren en nueva pestaña
    resultado = texto.replace(regexEnlace, '<a href="$&" target="_blank" rel="noopener noreferrer">$&</a>');
    // Reemplazar '*' con etiquetas <b>
    resultado = resultado.replace(regexBold, '<b>$1</b>')
    // Reemplazar '_' con etiquetas <i>
    resultado = resultado.replace(regexItalic, '<i>$1</i>')
    // reemplaza saltos de linea con <br>
    resultado = resultado.replaceAll('\n', '<br>');
  
    return resultado;
  }

  // * Función para agregar un mensaje al contenedor de mensajes
  function agregarMensaje(data) {
    console.log(data);
    const { remitenteId, isPropio } = data;
    console.log("remitenteId: ", remitenteId);
    console.log("isPropio: ", isPropio);
    const chatMessages = document.getElementById("chat-messages");
    const mensajeElemento = document.createElement("div");
    mensajeElemento.className = "chat-message";

    const bubbleElemento = document.createElement("div");
    bubbleElemento.className = `chat-bubble ${isPropio ? 'own' : 'other'}`;

    // * --- --- es texto
    if (data.hasOwnProperty('mensaje')) {
      const mensaje = data.mensaje;
      console.log("mensaje ===> ", mensaje);
      bubbleElemento.innerHTML = formatearTexto(mensaje);

      // Validar el contenido del mensaje
      const regexAdjuntar = /<strong>Adjuntar documento:<\/strong>/;
      const regexAdjuntoNoValido = /<strong>El documento adjunto no es válido.<\/strong>/;
      const btnAdjunto = document.getElementById('btnAdjunto');

      // Remover d-none si coincide con cualquiera de los regex
      if (regexAdjuntar.test(mensaje) || regexAdjuntoNoValido.test(mensaje)) {
        btnAdjunto.classList.remove('d-none'); // Remover d-none si coincide
      } else {
        btnAdjunto.classList.add('d-none'); // Asegurar que tenga d-none si no coincide
      }

      mensajeElemento.appendChild(bubbleElemento);
      chatMessages.appendChild(mensajeElemento);
    }
    // // * --- --- es texto
    // if (data.hasOwnProperty('mensaje')) {
    //   const mensaje = data.mensaje;
    //   console.log("mensaje ===> ", mensaje);
    //   bubbleElemento.innerHTML = formatearTexto(mensaje);

    //   // Validar el contenido del mensaje
    //   const regexAdjuntar = /<strong>Adjuntar documento:<\/strong>/;
    //   const regexAdjuntoNoValido = /<strong>El documento adjunto no es válido.<\/strong>/;
    //   const btnAdjunto = document.getElementById('btnAdjunto');

    //   // Remover d-none si coincide con cualquiera de los regex
    //   if (regexAdjuntar.test(mensaje) || regexAdjuntoNoValido.test(mensaje)) {
    //     btnAdjunto.classList.remove('d-none'); // Remover d-none si coincide
    //   } else {
    //     btnAdjunto.classList.add('d-none'); // Asegurar que tenga d-none si no coincide
    //   }

    //   mensajeElemento.appendChild(bubbleElemento);
    //   chatMessages.appendChild(mensajeElemento);
    // }

    console.log("antes validacion");
    // * --- --- es file
    // if (data.hasOwnProperty('fileData')) {
    //   console.log("antes validacion =====>", data.fileData);
    //   const { extFile, filename } = data.fileData;
    //   console.log("extFile: ", extFile);
    //   console.log("filename: ", filename);
    //   let contenido = '';

    //   // * Si tenemos archivo adjunto
    //   if (filename) {
    //     const arrImgTypes = ['jpeg', 'png', 'webp', 'jpg'];
    //     // const arrVideoTypes = ['mp4', 'avi'];
    //     const arrDocsTypes = ['pdf', 'doc', 'xls'];
    //     const srcFile = `${CHATWEB_URL}${filename}`;
    //     console.log("La ruta es: ", srcFile);

    //     if (arrImgTypes.includes(extFile)) contenido = `<img src="${srcFile}" style="cursor:pointer; width: 100%;" onclick="window.open(this.src)" />`;

    //     // if (arrVideoTypes.includes(extFile)) contenido = `<video src="${srcFile}" type="audio/mp3" controls style="width: 100%"></video>`;

    //     if (arrDocsTypes.includes(extFile)) contenido = `<a target="_blank" href="${srcFile}"><b><i class="bx bx-file"></i> ${filename} </b></a>`;

    //     // if (['ogg', 'mp3'].includes(extFile)) contenido = `<audio src="${srcFile}" type="audio/mp3" controls style="width: 100%"></audio>`;

    //     bubbleElemento.innerHTML = contenido;
    //   } else {
    //     bubbleElemento.innerHTML = `
    //       <strong>⚠️ *El documento adjunto no es válido.</strong> <br>
    //       <i>⚠️ El documento debe ser un archivo .pdf, .xls, .jpg, .png, .doc únicamente y no debe superar los 5 MB.</i>
    //     `;
    //   }
    // }

    // mensajeElemento.appendChild(bubbleElemento);
    // chatMessages.appendChild(mensajeElemento);

    if (data.hasOwnProperty('mensaje')) scrollBottomChat();
    if (data.hasOwnProperty('fileData')) setTimeout(() => { scrollBottomChat() }, 1500);
    hidechatbar()
  }

  // Manejo del evento click en el botón de enviar
  document.getElementById("send-button").addEventListener("click", () => {
    enviarTexto();
  });

  // Manejo del evento keydown en el cuadro de texto
  document
    .getElementById("message-input")
    .addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        enviarTexto();
      }
    });

  // Manejo del evento click en el botón de emojis
  document.getElementById("emoji-button").addEventListener("click", () => {
    toggleEmojiPicker();
  });

  // Función para mostrar u ocultar el selector de emojis
  function toggleEmojiPicker() {
    const emojiPicker = document.getElementById("emoji-picker");
    estado = emojiPicker.getAttribute("style");
    if (estado == "display: none;") {
      emojiPicker.style.display = "block";
    } else {
      emojiPicker.style.display = "none";
    }
  }

  // Enviar el mensaje por http
  function enviarTexto() {
    document.getElementById("emoji-picker").style.display = "none";
    const messageInput = document.getElementById("message-input");
    const mensaje = messageInput.value.trim();
    if (mensaje !== "") {
      agregarMensaje({ mensaje, clientId, isPropio: true });
      const texto = mensaje + ";;_;" + clientId;
      messageInput.value = "";
      // Enviar el texto al servidor Flask
      enviarTextoAlServidor(texto);
    }
  }

  function enviarTextoAlServidor(texto) {
    const url = `${BOTCHATWEBHOOK_URL}/inMessage`; // Reemplaza con la URL de tu servidor Flask

    axios
      .post(url, {
        texto: texto,
      })
      .then((response) => {
        console.log(response.data); // Respuesta del servidor Flask
      })
      .catch((error) => {
        console.error(error);
      });
  }

  // Guardar el ID de cliente en el almacenamiento local
  socket.on("connect", () => {
    clientId = socket.id;
    // console.log(clientId);
    if (clientId != null) {
      localStorage.setItem("clientId", clientId);
    }
  });

  function scrollBottomChat() {
    hidechatbar()
    const ultimoMensaje = document.querySelector('#chat-messages').lastChild.lastChild;
    ultimoMensaje.scrollIntoView({ behavior: "smooth", block: "end" });
  }

  // const pickerOptionsSelect = { onSelect: addEmojiToInput };
  // const pickerSelect = new EmojiMart.EmojiPicker(pickerOptionsSelect);
  // document.getElementById("emoji-picker").appendChild(pickerSelect);

  // ! Mostrar el formulario y ocultar el chat
  // const chatContainer = document.querySelector(".chat-container");
  // const formulario = document.getElementById("formulario");

  // chatContainer.style.display = "none";
  // document
  //   .getElementById("enviar-formulario")
  //   .addEventListener("click", (event) => {
  //     event.preventDefault();
  //     if (validarFormulario()) {
  //       formulario.style.display = "none";
  //       chatContainer.style.display = "block";
  //     }
  //   });

  // Validar el formulario
  function validarFormulario() {
    const validacion = validarDatosFormulario();
    if (validacion === true) {
      const nombreInput = document.getElementById("nombre-input");
      const documentoInput = document.getElementById("documento-input");
      const paisInput = document.getElementById("pais");
      const ciudadInput = document.getElementById("ciudad");
      const telefonoInput = document.getElementById("telefono-input");
      const correoInput = document.getElementById("correo-input");
      // const numeroCuentaInput = document.getElementById("numero-cuenta-input");
      // const mensajeInput = document.getElementById("mensaje-input");

      // Verificar que los campos no estén vacíos
      if (
        nombreInput.value.trim() === "" ||
        documentoInput.value.trim() === "" ||
        paisInput.value.trim() === "" ||
        ciudadInput.value.trim() === "" ||
        telefonoInput.value.trim() === "" ||
        correoInput.value.trim() === ""
        // numeroCuentaInput.value.trim() === "" ||
        // mensajeInput.value.trim() === ""
      ) {
        alert("Por favor, complete todos los campos del formulario.");
        return false;
      }

      return true;
    }
    return false;
  }

  // Función de validación del formulario
  function validarDatosFormulario() {
    // Obtener los valores de los campos del formulario
    /* const numeroCuenta = document.getElementById("numero-cuenta-input").value.trim(); */
    const nombre = document.getElementById("nombre-input").value.trim();
    const pais = document.getElementById("pais").value;
    const ciudad = document.getElementById("ciudad").value;
    const documento = document.getElementById("documento-input").value.trim();
    const telefono = document.getElementById("telefono-input").value.trim();
    const paisSelect = document.getElementById('pais');
    const correo = document.getElementById("correo-input").value.trim();
    const selectedOption = paisSelect.options[paisSelect.selectedIndex];
    const indicativo = selectedOption.getAttribute('data-code');
    /* const telconind = indicativo + telefono
    console.log(telconind) */
    // const mensaje = document.getElementById("mensaje-input").value.trim();
    // const terminos = document.getElementById("terminos-input").checked;

    // Expresiones regulares para las validaciones
    const regexTelefono = /^[0-9]{10}$/; // Número de teléfono colombiano de 10 dígitos
    const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Formato de correo electrónico válido
    const regexNumeros = /^[0-9]+$/; // Solo números
    const regexLetras = /^[a-zA-Z\s]+$/; // Solo letras

    // Validar cada campo del formulario
    const errores = [];

    /*
    if (numeroCuenta === "") {
        errores.push("El NIC es requerido");
    }
    */

    if (nombre === "") {
      errores.push("El nombre es requerido");
    } else if (!regexLetras.test(nombre)) {
      errores.push("El nombre solo puede contener letras");
    }

    if (pais === "") {
      errores.push("Seleccione el País");
    }

    if (ciudad === "") {
      errores.push("Seleccione la ciudad");
    }

    if (documento === "") {
      errores.push("El documento es requerido");
    } else if (!regexNumeros.test(documento)) {
      errores.push("El documento debe ser un número");
    }

    if (telefono === "") {
      errores.push("El teléfono es requerido");
    } /* else if (!regexTelefono.test(telefono)) {
      errores.push("El teléfono debe ser un número de 10 dígitos");
    } */

    if (correo === "") {
      errores.push("El correo electrónico es requerido");
    } else if (!regexCorreo.test(correo)) {
      errores.push("El correo electrónico no tiene un formato válido");
    }

    /*
    if (mensaje === "") {
        errores.push("Escriba un comentario");
    }
  
    if (!terminos) {
        errores.push("Debe aceptar los términos y condiciones");
    }
    */

    // Mostrar los errores o enviar el formulario
    if (errores.length > 0) {
      alert("Por favor corrija los siguientes errores:\n\n" + errores.join("\n"));
      return false;
    } else {
      // Aquí puedes enviar los datos si todo es válido
      enviarFormulario(clientId, nombre, pais, ciudad, documento, telefono, correo, indicativo);
      return true;
    }
  }


  // * Asignar la función de validación al evento submit del formulario
  document.getElementById("formulario").addEventListener("submit", validarFormulario);

  function enviarFormulario(
    clientId,
    nombre,
    pais,
    ciudad,
    documento,
    telefono,
    correo,
    indicativo
  ) {
    const url = `${BOTCHATWEBHOOK_URL}/sendForm`; // Reemplaza con la URL de tu servidor Flask

    axios
      .post(url, {
        clientId: clientId,
        nombre: nombre,
        pais: pais,
        ciudad: ciudad,
        documento: documento,
        telefono: telefono,
        correo: correo,
        indicativo: indicativo
      })
      .then((response) => {
        console.log(response.data); // Respuesta del servidor Flask
      })
      .catch((error) => {
        console.error(error);
      });
  }

  const inputs = document.querySelectorAll('input, select');

  inputs.forEach(input => {
    input.addEventListener('focus', () => {
      const aviso = input.nextElementSibling;
      if (aviso && aviso.classList.contains('aviso')) {
        aviso.style.display = 'block';
      }
    });

    input.addEventListener('blur', () => {
      const aviso = input.nextElementSibling;
      if (aviso && aviso.classList.contains('aviso')) {
        aviso.style.display = 'none';
      }
    });
  });
});

function validarLongitudMaxima(input, maxLength) {
  if (input.value.length > maxLength) {
    input.value = input.value.slice(0, maxLength);
  }
}

function formatearTexto(texto) {
  // Expresión regular para detectar enlaces
  const regexEnlace = /(http[s]?:\/\/[^\s]+)/g;
  const regexBold = /\*(.*?)\*/g;
  const regexItalic = /\_(.*?)\_/g;
  let resultado = '';

  // Reemplazar enlaces con etiquetas <a>
  resultado = texto.replace(regexEnlace, '<a href="$&">$&</a>');
  // Reemplazar '*' con etiquetas <b>
  resultado = resultado.replace(regexBold, '<b>$1</b>')
  // Reemplazar '_' con etiquetas <i>
  resultado = resultado.replace(regexItalic, '<i>$1</i>')
  // reemplaza saltos de linea con <br>
  resultado = resultado.replaceAll('\n', '<br>');

  return resultado;
}

function actualizarIndicativoYBandera() {
  const paisSelect = document.getElementById('pais');
  const selectedOption = paisSelect.options[paisSelect.selectedIndex];
  const indicativo = selectedOption.getAttribute('data-code');
  const bandera = selectedOption.getAttribute('data-flag');

  document.getElementById('indicativo').innerText = indicativo ? indicativo + ' ' : '';
  document.getElementById('bandera').innerText = bandera ? bandera : '';
}

function validarLongitudMaxima(input, maxLength) {
  if (input.value.length > maxLength) {
    input.value = input.value.slice(0, maxLength);
  }
}

function actualizarCiudades() {
  var pais = document.getElementById('pais').value;
  var ciudadSelect = document.getElementById('ciudad');

  if (pais) {
    // Realiza una petición GET a la API para obtener las ciudades
    fetch('/ciudades?pais=' + encodeURIComponent(pais))
      .then(response => response.json())
      .then(ciudades => {
        ciudadSelect.innerHTML = "<option value='' disabled selected>Ciudad</option>";
        ciudades.forEach(ciudad => {
          var option = document.createElement('option');
          option.value = ciudad;
          option.textContent = ciudad;
          ciudadSelect.appendChild(option);
        });
      })
      .catch(error => console.error('Error:', error));
  } else {
    ciudadSelect.innerHTML = "<option value=''>Ciudad</option>";
  }
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
    document.getElementById("location").innerHTML = "La geolocalización no es compatible con este navegador.";
  }
}

function showPosition(position) {
  document.getElementById("location").innerHTML =
    "Latitud: " + position.coords.latitude +
    "<br>Longitud: " + position.coords.longitude;
}

function showError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      document.getElementById("location").innerHTML = "El usuario negó el permiso para obtener la ubicación.";
      break;
    case error.POSITION_UNAVAILABLE:
      document.getElementById("location").innerHTML = "La ubicación no está disponible.";
      break;
    case error.TIMEOUT:
      document.getElementById("location").innerHTML = "La solicitud para obtener la ubicación ha caducado.";
      break;
    case error.UNKNOWN_ERROR:
      document.getElementById("location").innerHTML = "Ha ocurrido un error desconocido.";
      break;
  }
}