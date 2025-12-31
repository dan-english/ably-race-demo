from flask import Flask, send_from_directory, jsonify
import os, subprocess, json
import threading


# Point to the Vue build folder inside frontend
app = Flask(__name__, static_folder="./dist")
template_folder = "./dist"

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    file_path = os.path.join(app.static_folder, path)

    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)

    return send_from_directory(template_folder, "index.html")



DIST_FOLDER = os.path.abspath("./dist")  # root-level dist folder
# Helper function for serving a single HTML file
def serve_html(html_file):
    return send_from_directory(DIST_FOLDER, html_file)

# Dashboard Vue app
@app.route("/dashboard", defaults={"path": ""})
@app.route("/dashboard/<path:path>")
def serve_vue_dashboard(path):
    file_path = os.path.join(DIST_FOLDER, path)
    # Only serve static files if they exist in dist
    if path != "" and os.path.exists(file_path):
        return send_from_directory(DIST_FOLDER, path)
    return serve_html("dashboard.html")  # explicitly serve dashboard.html



# Docs Vue app
@app.route("/docs", defaults={"path": ""})
@app.route("/docs/<path:path>")
def serve_vue_docs(path):
    file_path = os.path.join(DIST_FOLDER, path)
    # Only serve static files if they exist in dist
    if path != "" and os.path.exists(file_path):
        return send_from_directory(DIST_FOLDER, path)
    return serve_html("docs.html")  # explicitly serve docs.html



# Debug Vue app
@app.route("/debug", defaults={"path": ""})
@app.route("/debug/<path:path>")
def serve_vue_debug(path):
    file_path = os.path.join(DIST_FOLDER, path)
    # Only serve static files if they exist in dist
    if path != "" and os.path.exists(file_path):
        return send_from_directory(DIST_FOLDER, path)
    return serve_html("debug.html")  # explicitly serve docs.html


# Rewind Vue app
@app.route("/rewind", defaults={"path": ""})
@app.route("/rewind/<path:path>")
def serve_vue_rewind(path):
    file_path = os.path.join(DIST_FOLDER, path)
    # Only serve static files if they exist in dist
    if path != "" and os.path.exists(file_path):
        return send_from_directory(DIST_FOLDER, path)
    return serve_html("rewind.html")  # explicitly serve docs.html


# History Vue app
@app.route("/history", defaults={"path": ""})
@app.route("/history/<path:path>")
def serve_vue_history(path):
    file_path = os.path.join(DIST_FOLDER, path)
    # Only serve static files if they exist in dist
    if path != "" and os.path.exists(file_path):
        return send_from_directory(DIST_FOLDER, path)
    return serve_html("history.html")  # explicitly serve docs.html


def run_script_background():
    subprocess.run(['python', 'race/race4.py'])


@app.route('/api/run-script', methods=['POST'])
def run_script():
    thread = threading.Thread(target=run_script_background)
    thread.start()

    return jsonify({
        'success': True,
        'message': 'Script started in background'
    })



if __name__ == "__main__":
    app.run(debug=True)
