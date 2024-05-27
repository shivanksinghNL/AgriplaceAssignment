from flask import Flask, jsonify, render_template
from main import PackageManager

app = Flask(__name__)
package_manager = PackageManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/packages', methods=['GET'])
def get_packages():
    try:
        return jsonify(list(package_manager.package_dict.keys()))
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/packages/<package_name>', methods=['GET'])
def get_package_details(package_name):
    try:
        package = package_manager.package_dict.get(package_name)
        if not package:
            return jsonify(error=f'Package {package_name} not found'), 400

        details = {
            'name': package.get('Package'),
            'description': package.get('Description'),
            'dependencies': package_manager.get_dependencies(package_name),
            'reverse_dependencies': package_manager.get_reverse_dependencies(package_name)
        }

        return jsonify(details)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)