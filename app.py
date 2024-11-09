from flask import Flask, render_template, request, jsonify
import plotly.express as px
import plotly.io as pio
import pandas as pd
import datetime

app = Flask(__name__)

# Funzione per caricare e generare i grafici
def generate_graphs():
    # Carica i dati dal file CSV
    df = pd.read_csv("records.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Crea i grafici per ciascuna feature
    graphs = {}
    features = ["Temperature", "Humidity", "CO2", "PM2.5", "TVOC", "PM1", "PM10", "AQI"]
    titles = ["Temperatura", "Umidità", "CO2", "PM2.5", "TVOC", "PM1", "PM10", "AQI"]

    for feature, title in zip(features, titles):
        fig = px.line(df, x="Timestamp", y=feature, title=f"Andamento {title}")
        graphs[feature] = pio.to_html(fig, full_html=False)
    
    return graphs

@app.route("/")
def home():
    graphs = generate_graphs()
    return render_template("index.html", graphs=graphs)

# Endpoint per ricevere nuovi dati
@app.route("/update_data", methods=["POST"])
def update_data():
    # Estrai i dati dalla richiesta JSON
    data = request.json
    if not data:
        return jsonify({"error": "Dati mancanti"}), 400
    
    # Aggiungi un nuovo record a records.csv
    try:
        # Estrai il timestamp attuale se non è fornito
        timestamp = data.get("Timestamp", datetime.datetime.now().isoformat())
        new_data = {
            "Timestamp": timestamp,
            "Temperature": data["Temperature"],
            "Humidity": data["Humidity"],
            "CO2": data["CO2"],
            "PM2.5": data["PM2.5"],
            "TVOC": data["TVOC"],
            "PM1": data["PM1"],
            "PM10": data["PM10"],
            "AQI": data["AQI"]
        }
        
        # Aggiungi il nuovo record al file CSV
        df = pd.DataFrame([new_data])
        df.to_csv("records.csv", mode="a", header=False, index=False)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
