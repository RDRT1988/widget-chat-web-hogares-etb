// ! VARIABLES GLOBALES
// ? Garantizar estos valores segun el .env principal

const CHATWEB_URL = 'http://localhost:8000'
const AUTENTICACION_URL = 'http://localhost:8002'


document.addEventListener('DOMContentLoaded', async () => {
  const contenedorWidget = document.querySelector('#cont-widget-chat-bot');

  const contenidoWidget = `
    <div id='widgetChatBot'>
    <div id='contChat' class='cont-chat'>
      <div class='bar-chat'>
        <div class='bar-box bar-box1' style="flex-grow: 1">
          <img class="bar-img" src='${CHATWEB_URL}/img/logo_sistema_sm.png' alt=''>
        </div>

        <div class='bar-box bar-box2' style="flex-grow: 2">
          <span id="tituloChatWeb">MEETINGS ETB</span>
          <span id="estadoChatWeb">
            <i class="material-icons">brightness_1</i> Online
          </span>
        </div>
        <div class='bar-box bar-box3' style="flex-grow: 1">
          <i id='btnMinimizar' class="material-icons">remove</i>
          <i id='btnCerrar' class="material-icons">close</i>
        </div>

      </div>

      <div class='main-chat'>
        <iframe id='ifrChat' frameborder='0'></iframe>
      </div>

    </div>

    <div id='btnToggleChat' class='btn-chat-pau'>
      <img class='img-btn' src='${CHATWEB_URL}/img/widget.png' alt=''>  
    </div>
  </div>`;

  contenedorWidget.innerHTML = contenidoWidget;

  const btnToggleChat = document.querySelector('#widgetChatBot #btnToggleChat');
  const btnMinimizar = document.querySelector('#widgetChatBot #btnMinimizar');
  const btnCerrar = document.querySelector('#widgetChatBot #btnCerrar');
  const contChat = document.querySelector('#widgetChatBot #contChat');
  const ifrChat = document.querySelector('#widgetChatBot #ifrChat');

  const getJWT = async () => {
    const response = await fetch(`${AUTENTICACION_URL}/get-jwt`);
    const data = await response.json();
    return data.token;
  };

  btnToggleChat.addEventListener('click', async () => {
    const token = await getJWT();
    const chatURL = `${CHATWEB_URL}/chat?token=${token}`;
    ifrChat.src = chatURL;
    contChat.style.animationName = 'ani-open-chat';
    contChat.style.display = 'block';
  });

  btnMinimizar.addEventListener('click', () => {
    contChat.style.animationName = 'ani-close-chat';
  });

  btnCerrar.addEventListener('click', () => {
    ifrChat.src = ifrChat.src; // lo reinicia
    contChat.style.animationName = 'ani-close-chat';
  });
});
