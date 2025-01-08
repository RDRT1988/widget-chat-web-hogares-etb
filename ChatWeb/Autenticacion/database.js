const mysql = require("mysql2");
const dotenv = require('dotenv');
const path = require('path');
const Class2 = require("./Class2");

//Cargar archivo .env
dotenv.config({ path: path.join(__dirname, '..', '..', '.env') });

let conn = mysql.createConnection({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT),
  user: process.env.DB_USER,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  dateStrings: true,
});


try {
  conn.query("SELECT 1");
  console.log(`Conectado a DB: ${process.env.DB_NAME} `);
  const sql = "SELECT 1";
  setInterval(() => {
    conn
      .promise()
      .query(sql)
      .then(([result, fields]) => {
        console.log("Conexion a DB correcta");
      })
      .catch((err) => console.log("ERROR::", err));
  }, 3600000);
} catch (error) {
  if (error) {
    let posicion = error.message.indexOf("Can't add new command when connection is in closed state");
    if (posicion !== -1) {
      console.log("Desconectado de DB");
      conn = mysql.createConnection({
        host: process.env.DB_HOST,
        port: parseInt(process.env.DB_PORT),
        user: process.env.DB_USER,
        database: process.env.DB_NAME,
        password: process.env.DB_PASSWORD,
        dateStrings: true,
      });
      console.log("Reconectado a DB ");
    }
  }
}

module.exports = conn;
