from flask import Flask, jsonify
from main import PackageManager


app = Flask(__name__)
package_manager = PackageManager()

@app.route('/packages', methods=['GET'])
def get_packages():
    package_names = [pkg['Package'] for pkg in package_manager.packages_list]
    return jsonify(package_names)



if __name__ == '__main__':
    app.run(debug=True)