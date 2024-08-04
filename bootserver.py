from Application import create_app
from instance import Deployment, Development
import os

directory = 'instance'
extensions = ('.db', '.sqlite')

if os.path.isdir(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path) and filename.endswith(extensions):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
else:
    print(f"The directory '{directory}' does not exist.")

wsgiapp = create_app(Deployment())

if __name__ == '__main__':
    wsgiapp = create_app(Development())
    wsgiapp.run(debug=True, host='0.0.0.0', port=5000, ssl_context="adhoc")