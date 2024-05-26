from flask import Flask, jsonify, abort
from main import PackageManager

app = Flask(__name__)
package_manager = PackageManager()

@app.route('/packages', methods=['GET'])
def get_packages():
    package_names = [pkg['Package'] for pkg in package_manager.packages_list]
    return jsonify({"packages": package_names} )

@app.route('/packages/<package_name>', methods=['GET'])
def get_package_details(package_name):
    package = package_manager.package_dict.get(package_name)
    if not package:
        abort(400, "Package name is not correct")

    details = {
        'name': package.get('Package'),
        'description': package.get('Description'),
        'dependencies': package_manager.get_dependencies(package_name),
        'reverse_dependencies': package_manager.get_reverse_dependencies(package_name)
    }

    return jsonify(details)


if __name__ == '__main__':
    app.run(debug=True)