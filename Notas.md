Credenciales de la antigua base de datos:


export PYTHON_ENV='gcf'
export PG_HOST='34.136.98.250'
export PG_PORT='5432'
export PG_USER='postgres'
export PG_PASS='1234AB'
export PG_NAME='postgres'
export FLASK_SECRET_KEY='tu_clave_secreta_aqui'

Cuenta de paypal donde se crearon estas credenciales de certus:
Cuenta de Paypal de Pruebas:

Correo: sb-spxvk28518120@personal.example.com
Contraseña: 4]+XndR$


Comandos Postgres SQL para replicar todas las tablas y columnas: 

CREATE TABLE usuarios (
  id integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  username varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  profile_picture bytea,
  email varchar(255) NOT NULL,
  profile_picture_path varchar(255)
);

CREATE TABLE comentarios (
  id SERIAL PRIMARY KEY,  -- Auto-incrementing primary key in PostgreSQL
  usuario_id INT NOT NULL,
  comentario TEXT NOT NULL,
  fecha TIMESTAMP NOT NULL,
  user_timezone VARCHAR(50)
);


CREATE TABLE productos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT,
  precio NUMERIC(10,2) NOT NULL,
  imagen VARCHAR(255),
  categoria VARCHAR(50)
);

CREATE TABLE carts (
  cart_id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  product_id INTEGER,
  total_price DECIMAL(10,2),
  is_purchased_cart BOOLEAN DEFAULT FALSE
);

CREATE TABLE cart_details (
  id SERIAL PRIMARY KEY,
  cart_id INTEGER NOT NULL,
  product_id INTEGER,
  quantity INTEGER,
  total_price DECIMAL(10,2),
  username VARCHAR(255) NOT NULL,
  is_purchased_cart BOOLEAN DEFAULT FALSE
);

CREATE TABLE contacto (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  mensaje TEXT
);
