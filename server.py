from flask import render_template
import config

conn_app = config.conn_app

# lee archivo swagger.yml para configurar rutas
conn_app.add_api("swagger.yml")

# crea ruta raiz
@conn_app.route("/")
def home():
    """
    servidor en localhost:5000

    :return:  home. html renderizado de templates
    """
    return render_template("home.html")


if __name__ == "__main__":
    conn_app.run(debug=True)
