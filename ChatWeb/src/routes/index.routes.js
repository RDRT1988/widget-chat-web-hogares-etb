const router = require("express").Router();
const jwt = require('jsonwebtoken');
const Class2 = require('../Class2');
const dotenv = require('dotenv');
const path = require('path');
const mysql = require('mysql');
const fs = require('fs');

//Cargar archivo .env
dotenv.config({ path: path.join(__dirname, '..', '..', '..', '.env') });

// Configuración de la conexión a la base de datos
const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

db.connect((err) => {
  if (err) {
    console.error('Error al conectar a la base de datos:', err);
    return;
  }
  console.log('Conexión a la base de datos establecida.');
});

// Clave secreta usada para firmar y verificar el token
const secretKey = process.env.SECRET_KEY;

// Middleware para verificar el token JWT
const verifyToken = (req, res, next) => {
  const token = req.query.token;

  if (!token) {
    return res.status(403).send('Token is required');
  }

  jwt.verify(token, secretKey, (err, decoded) => {
    if (err) {
      return res.status(401).send('Invalid token');
    }
    // Si el token es válido, pasa al siguiente middleware o ruta
    next();
  });
};

// Redirige a la ruta /chat
router.get("/", (req, res) => {
  res.redirect('/chat');
});

// Aplica el middleware de verificación antes de acceder al chat
router.get("/chat", verifyToken, (req, res) => {
  res.render('chat/chat', { title: 'Web Chat' });
});

// Ruta para obtener las ciudades según el país
router.get('/ciudades', (req, res) => {
  const pais = req.query.pais;

  if (!pais) {
    return res.status(400).json({ error: 'El país es requerido' });
  }

  const query = 'SELECT nombre_ciudad FROM tbl_ciudades WHERE nombre_pais = ?';
  db.query(query, [pais], (err, results) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }

    const ciudades = results.map(row => row.nombre_ciudad);
    res.json(ciudades);
  });
});


// ! OBTENER ADJUNTO CHAT WEB
  // router.get('/adjuntoChatWeb', async (req, res) => {
  //   console.log('Adjunto Chat Web');
  //   console.log('req.query', req.query);

  //   // * Variables
  //   const {idRegistro} = req.query;
  //   console.log('idRegistro', idRegistro);

  //   try {
  //     if (!idRegistro) {
  //       return res.status(400).json({
  //         status: 400,
  //         type: 'warning',
  //         title: 'Chat Web Segmento 4',
  //         message: 'El idRegistro es requerido'
  //       });
  //     }

  //     // * Query
  //     const query = `
  //         SELECT SQL_NO_CACHE
  //         cht_adjuntos AS ADJUNTO,
  //         cht_ruta_archivo_adjunto AS RUTA_ARCHIVO_ADJUNTO 
  //       FROM 
  //         tbl_chat 
  //       WHERE
  //         cht_id = ?
  //     `;
  //     // Envolver db.query en una promesa
  //     const result = await new Promise((resolve, reject) => {
  //       db.query(query, [idRegistro], (err, results) => {
  //         if (err) {
  //           return reject(err);
  //         }
  //         resolve(results[0]); // Asegúrate de devolver el primer resultado
  //       });
  //     });
  //     console.log('result', result);
      
  //     // * Enviar respuesta
  //     if (result.ADJUNTO === 'Si') {
  //       // todo: si hay adjunto
  //       // ? Obtener el archivo adjunto
  //       const archivoAdjunto = await fs.readFile(path.join(process.env.RUTA_CARPETA_DOCS, result.RUTA_ARCHIVO_ADJUNTO));
  //       console.log('archivoAdjunto', archivoAdjunto);
  //       const linkArchivoAdjunto = process.env.CHATWEB_URL + result.RUTA_ARCHIVO_ADJUNTO;
  //       console.log('linkArchivoAdjunto', linkArchivoAdjunto);

  //       // ? Armar respuesta
  //       const respuesta = {
  //         adjunto: result.ADJUNTO,
  //         linkArchivoAdjunto: linkArchivoAdjunto,
  //         archivoAdjunto: archivoAdjunto
  //       }
  //       return res.status(200).json({
  //         status: 200,
  //         type: 'success',
  //         title: 'Chat Web Segmento 4',
  //         message: 'Archivo Adjunto del Chat',
  //         data: respuesta
  //       });
  //     } else {
  //       // todo: si no  hay adjunto
  //       // * Armar respuesta
  //       const respuesta = {
  //         adjunto: result.ADJUNTO,
  //         linkArchivoAdjunto: null,
  //         archivoAdjunto: null
  //       }
  //       return res.status(200).json({
  //         status: 200,
  //         type: 'success',
  //         title: 'Chat Web Segmento 4',
  //         message: 'No hay archivo adjunto',
  //         data: respuesta
  //       });
  //     }
  //   } catch (error) {
  //     console.log('❌ Error en ChatWeb/src/routes/index.routes.js → adjuntoChatWeb', error);
  //     res.status(500).json({
  //       status: 500,
  //       type: 'error',
  //         title: 'Chat Web Segmento 4',
  //         message: 'No se pudo obtener el archivo adjunto, por favor intenta de nuevo o comunícate con nosotros.',
  //         error: error.message
  //     });
  //   }
  // });
// // ! OBTENER ADJUNTO CHAT WEB
// router.get('/adjuntoChatWeb', async (req, res) => {
//   console.log('Adjunto Chat Web');
//   console.log('req.query', req.query);

//   // * Variables
//   const {idRegistro} = req.query;
//   console.log('idRegistro', idRegistro);

//   try {
//     if (!idRegistro) {
//       return res.status(400).json({
//         status: 400,
//         type: 'warning',
//         title: 'Chat Web Segmento 4',
//         message: 'El idRegistro es requerido'
//       });
//     }

//     // * Query
//     const query = `
//         SELECT SQL_NO_CACHE
//         cht_adjuntos AS ADJUNTO,
//         cht_ruta_archivo_adjunto AS RUTA_ARCHIVO_ADJUNTO 
//       FROM 
//         tbl_chat 
//       WHERE
//         cht_id = ?
//     `;
//     // Envolver db.query en una promesa
//     const result = await new Promise((resolve, reject) => {
//       db.query(query, [idRegistro], (err, results) => {
//         if (err) {
//           return reject(err);
//         }
//         resolve(results[0]); // Asegúrate de devolver el primer resultado
//       });
//     });
//     console.log('result', result);
    
//     // * Enviar respuesta
//     if (result.ADJUNTO === 'Si') {
//       // todo: si hay adjunto
//       const filePath = path.join(process.env.RUTA_CARPETA_DOCS, result.RUTA_ARCHIVO_ADJUNTO); // Ruta completa del archivo
//       console.log('Ruta del archivo:', filePath); // Imprimir la ruta para depuración

//       // Verificar si el archivo existe antes de intentar enviarlo
//       fs.access(filePath, fs.constants.F_OK, (err) => {
//         if (err) {
//           console.error('El archivo no existe:', err);
//           return res.status(404).json({
//             status: 404,
//             type: 'error',
//             title: 'Chat Web Segmento 4',
//             message: 'El archivo solicitado no existe.'
//           });
//         }

//         // Enviar el archivo
//         res.sendFile(filePath, (err) => {
//           if (err) {
//             console.log('Error al enviar el archivo:', err);
//             res.status(err.status).end();
//           } else {
//             console.log('Archivo enviado:', filePath);
//           }
//         });
//       });
//     } else {
//       // todo: si no  hay adjunto
//       // * Armar respuesta
//       const respuesta = {
//         adjunto: result.ADJUNTO,
//       }
//       return res.status(200).json({
//         status: 200,
//         type: 'success',
//         title: 'Chat Web Segmento 4',
//         message: 'No hay archivo adjunto',
//         data: respuesta
//       });
//     }
//   } catch (error) {
//     console.log('❌ Error en ChatWeb/src/routes/index.routes.js → adjuntoChatWeb', error);
//     res.status(500).json({
//       status: 500,
//       type: 'error',
//       title: 'Chat Web Segmento 4',
//       message: 'No se pudo obtener el archivo adjunto, por favor intenta de nuevo o comunícate con nosotros.',
//       error: error.message
//     });
//   }
// });

// ! OBTENER ADJUNTO CHAT WEB
router.get('/adjuntoChatWeb', async (req, res) => {
  console.log('Adjunto Chat Web');
  console.log('req.query', req.query);

  // * Variables
  const {idRegistro} = req.query;
  console.log('idRegistro', idRegistro);

  try {
    if (!idRegistro) {
      return res.status(400).json({
        status: 400,
        type: 'warning',
        title: 'Chat Web Segmento 4',
        message: 'El idRegistro es requerido'
      });
    }

    // * Query
    const query = `
        SELECT SQL_NO_CACHE
        cht_adjuntos AS ADJUNTO,
        cht_ruta_archivo_adjunto AS RUTA_ARCHIVO_ADJUNTO 
      FROM 
        tbl_chat 
      WHERE
        cht_id = ?
    `;
    // Envolver db.query en una promesa
    const result = await new Promise((resolve, reject) => {
      db.query(query, [idRegistro], (err, results) => {
        if (err) {
          return reject(err);
        }
        resolve(results);
      });
    });
    console.log('result', result);
    
    // * Enviar respuesta
    if (result && result.length > 0) {
      // todo: si hay resultados
      if (result[0].ADJUNTO === 'Si') {
        // todo: si hay adjunto
        const filePath = path.join(process.env.RUTA_CARPETA_DOCS, result[0].RUTA_ARCHIVO_ADJUNTO); // Ruta completa del archivo
        console.log('Ruta del archivo:', filePath); // Imprimir la ruta para depuración

        // Verificar si el archivo existe antes de intentar enviarlo
        fs.access(filePath, fs.constants.F_OK, (err) => {
          if (err) {
            console.error('El archivo no existe:', err);
            return res.status(404).json({
              status: 404,
              type: 'error',
              title: 'Chat Web Segmento 4',
              message: 'El archivo solicitado no existe.'
            });
          }

          // Crear el enlace al archivo
          const fileUrl = `${req.protocol}://${req.get('host')}${result[0].RUTA_ARCHIVO_ADJUNTO}`;
          console.log('fileUrl', fileUrl);

          // Enviar respuesta JSON con el enlace al archivo
          return res.status(200).json({
            status: 200,
            type: 'success',
            title: 'Chat Web Segmento 4',
            message: 'Archivo disponible.',
            data: {
              adjunto: result[0].ADJUNTO,
              linkArchivoAdjunto: fileUrl
            }
          });
        });
      } else {
        // todo: si no  hay adjunto
        const respuesta = {
          adjunto: result[0].ADJUNTO,
        }
        return res.status(200).json({
          status: 200,
          type: 'success',
          title: 'Chat Web Segmento 4',
          message: 'No hay archivo adjunto',
          data: respuesta
        });
      }
    } else {
      // todo: si no hay resultados
      return res.status(404).json({
        status: 404,
        type: 'error',
        title: 'Chat Web Segmento 4',
        message: 'No se encontraron resultados.'
      });
    }
  } catch (error) {
    console.log('❌ Error en ChatWeb/src/routes/index.routes.js → adjuntoChatWeb', error);
    res.status(500).json({
      status: 500,
      type: 'error',
      title: 'Chat Web Segmento 4',
      message: 'No se pudo obtener el archivo adjunto, por favor intenta de nuevo o comunícate con nosotros.',
      error: error.message
    });
  }
});

// ! EXPORTE
module.exports = router;

