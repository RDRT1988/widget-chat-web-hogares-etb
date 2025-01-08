'use strict';
const express = require('express');
const morgan = require('morgan');
const cors = require('cors');
const path = require('path');
const dotenv = require('dotenv');
const Class2 = require('./Class2');
const db = require("./database");
const jwt = require('jsonwebtoken');
const request = require('request');

const secretKey = process.env.SECRET_KEY;

//Cargar archivo .env
dotenv.config({ path: path.join(__dirname, '..', '..', '.env') });
const DB = process.env.DB_NAME;

//Inicio
const app = express();

//*settings */
app.set('PORT', parseInt(process.env.AUTENTICACION_PORT));
app.use(cors({ origin: '*' }));


// * Middleware
app.use(morgan('dev'));
app.use(express.json());

app.get('/get-jwt', (req, res) => {

    const token = jwt.sign({ user: 'user_id' }, secretKey, {
        expiresIn: '2s',
        algorithm: 'HS512'
    });

    res.json({ token });

});

app.post('/activarLlamada', async (req, res) => {

    const { id, pais, hora_actual, contacto } = req.body;

    const contactoExtracto = contacto.substring(0, 4);

    console.log(id, pais, hora_actual, contacto, "AAAAAAAAAAAAAAAAAAAAAAAAA");

    const url = `http://172.17.8.205/vicidial/non_agent_api.php?source=test&user=thom24&pass=1q8ScwG1wI1BEi6&function=add_lead&phone_number=${contactoExtracto}&list_id=40000&dnc_check=N&first_name=${pais}&last_name=${hora_actual}`;


    const options = {
        url: url,
        method: 'POST',
        strictSSL: false, // Deshabilita la verificación del certificado SSL
        headers: {
            "Content-Type": "application/json",
            "Authorization": "9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5",
            "X-UserId": "THOMASCHATWEB",
        }
    };

    const updategestion = `UPDATE ${DB}.tbl_chat SET GES_ESTADO_HORARIO = 'PRIMERA LLAMADA REALIZADA' WHERE PKGES_CODIGO = ${id};`;
    let [resultUpdate] = await db.promise().query(updategestion);

    request(options, (error, response, body) => {
        if (error) {
            console.error('Error en la solicitud:', error);
            res.status(500).json({ error: 'Error en la solicitud' });
        } else {
            if (response.statusCode === 200) {
                console.log('Datos enviados y procesados exitosamente');
                res.status(200).json({ message: 'Datos enviados y procesados exitosamente', body });
            } else {
                console.error(`Error al enviar los datos. Código de estado: ${response.statusCode} ${response.statusMessage}`);
                res.status(response.statusCode).json({ error: response.statusMessage, body });
            }
        }
    });
});


app.listen(app.get('PORT'), () => console.log('Servidor AUTENTICACION en puerto : ', app.get('PORT')));