const express = require("express");
const morgan = require('morgan');
// const app = express();
// const http = require("http").createServer(app);
const { Server } = require('socket.io')
const http = require('http');
// const io = require("socket.io")(http);
//const { apis } = require('../global.config');
const exphbs = require('express-handlebars');
const path = require('path');
const cors = require('cors');
const dotenv = require('dotenv');
//Cargar archivo .env
dotenv.config({ path: path.join(__dirname, '..', '..', '.env') });

// * init socketio
const app = express();
const server = http.createServer(app); // io
const io = new Server(server); // io

io.on("connection", (socket) => {

  console.log('Nueva conexión server', socket.id);
  // Obtener el ID de cliente anterior del query parameter o generar uno nuevo
  const previousClientId = socket.handshake.query.clientId;
  const clientId = previousClientId || socket.id;

  // Emitir evento 'cliente-anterior' con el ID de cliente anterior
  if (previousClientId) {
    console.log("Cliente anterior:", previousClientId);
    socket.emit("server_node:cliente-anterior", previousClientId);
  }

  // Enviar un mensaje al cliente nuevo que se conecta
  // socket.emit("server_node:mensaje", { mensaje: '📝 <strong>Para continuar por favor ingrese el número de NIT.</strong>\n\n ❌ <i>Sin dígito de verificación.</i>\n 🚫 <i>Sin espacios ni caracteres especiales.</i>\n 🔢 <i>Solo números.</i>', isFile: false, remitenteId: socket.io }, socket.io);

  // Manejo del evento 'mensaje' cuando se recibe un mensaje desde el cliente front
  socket.on("server_node:mensaje", (mensaje) => {
    // Emitir el mensaje a todos los clientes, excepto al remitente
    socket.broadcast.emit("mensaje", mensaje, clientId);
  });
  
  socket.on("prueba python", (mensaje) => {
    // Emitir el mensaje a todos los clientes, excepto al remitente
    console.log(mensaje)
  });
  // Manejo del evento 'mensaje' cuando se recibe un mensaje desde el cliente Python
  socket.on("server_py:mensaje", (data) => {
    console.log(data);
    if (data.hasOwnProperty('remitenteId')) {
      const { remitenteId } = data;
      io.to(remitenteId).emit("server_node:mensaje", data);
    } else {
      console.log("Mensaje incorrecto recibido desde el cliente Python", data);
    }
  });
});

// * public
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, '../node_modules/boxicons/')));
app.use(express.static(path.join(__dirname, '../node_modules/axios/dist/')));
app.use(express.static(path.join(__dirname, '../node_modules/emoji-mart/dist/')));
app.use(express.static(path.join(__dirname, '../node_modules/sweetalert2/dist')));
app.use(express.static(path.join(__dirname, '../node_modules/socket.io/client-dist/')));
app.use(express.static(path.join(__dirname, '../node_modules/bootstrap/dist/')));
app.use(express.static(path.join(__dirname, '../../WebHookWhasappConnetly/media')));
app.use(express.static(path.join(__dirname, '../../WebHookWhasappConnetly/receivedFiles')));
app.use(express.static(path.join(__dirname, '../../ChatWeb/docs')));

// * settings
//app.set('PORT', process.env.PORT || apis.chatWeb.port);
app.set('PORT', parseInt(process.env.CHATWEB_PORT));
app.set('views', path.join(__dirname, 'views'));
app.engine(
  '.hbs',
  exphbs.engine({
    defaultLayout: 'main',
    layoutsDir: path.join(app.get('views'), 'layouts'),
    partialsDir: path.join(app.get('views'), 'partials'),
    extname: '.hbs',
    helpers: require('./lib/handlebars'),
  })
);
app.set('view engine', '.hbs');


app.use(morgan('dev'));
app.use(cors({ origin: true }));
app.use(express.urlencoded({ extended: false })); // Aceptar datos sencillos
app.use(express.json());

// * routes
app.use(require('./routes/index.routes')); // esta ruta es -> index.js
// app.use('/preparacion', require('./routes/preparacion.routes')); ejemplo por si quiero agregar otra

// http.listen(app.get('PORT'), () => {
//   console.log(`Server on port ${app.get('PORT')} - http://localhost:${app.get('PORT')}`);
// });

server.listen(app.get('PORT'), () => {
  console.log(`Server on port ${app.get('PORT')} - http://localhost:${app.get('PORT')}`);
});

//console.log(apis.chatWeb.port);