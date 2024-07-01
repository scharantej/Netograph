
# Import necessary libraries
from flask import Flask, render_template, request
import googleapiclient.discovery
import uuid
import io
import os
import pydot

# Create a Flask application
app = Flask(__name__)

# Define the home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define the submit route
@app.route('/submit', methods=['POST'])
def submit():
    # Receive the request data
    project_id = request.form['project_id']

    # Generate a unique filename for the generated diagram
    filename = 'network_diagram' + str(uuid.uuid4())

    # Create a network graph and add nodes
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')

    # Add a node for the GCP project
    project_node = pydot.Node(project_id, shape='box', style='filled', fillcolor='lightblue')
    graph.add_node(project_node)

    # Fetch the GCP project details using the API
    compute = googleapiclient.discovery.build('compute', 'v1')
    networks = compute.networks().list(project=project_id).execute()
    subnetworks = compute.subnetworks().list(project=project_id).execute()
    instances = compute.instances().list(project=project_id).execute()
    firewalls = compute.firewalls().list(project=project_id).execute()

    # Add nodes for networks, subnetworks, and firewalls
    for network in networks:
        network_node = pydot.Node(network['name'], shape='oval', style='filled', fillcolor='yellow')
        graph.add_node(network_node)

    for subnetwork in subnetworks:
        subnetwork_node = pydot.Node(subnetwork['name'], shape='oval', style='filled', fillcolor='green')
        graph.add_node(subnetwork_node)

    for firewall in firewalls:
        firewall_node = pydot.Node(firewall['name'], shape='diamond', style='filled', fillcolor='red')
        graph.add_node(firewall_node)

    # Add nodes for instances
    for instance in instances:
        instance_node = pydot.Node(instance['name'], shape='box', style='filled', fillcolor='lightblue')
        graph.add_node(instance_node)

    # Connect nodes based on relationships
    for instance in instances:
        for network in networks:
            if instance['networkInterfaces'][0]['network'] == network['selfLink']:
                instance_node = graph.get_node(instance['name'])
                network_node = graph.get_node(network['name'])
                graph.add_edge(pydot.Edge(instance_node, network_node))

    for subnetwork in subnetworks:
        for network in networks:
            if subnetwork['network'] == network['selfLink']:
                subnetwork_node = graph.get_node(subnetwork['name'])
                network_node = graph.get_node(network['name'])
                graph.add_edge(pydot.Edge(subnetwork_node, network_node))

    for firewall in firewalls:
        for network in networks:
            if firewall['network'] == network['selfLink']:
                firewall_node = graph.get_node(firewall['name'])
                network_node = graph.get_node(network['name'])
                graph.add_edge(pydot.Edge(firewall_node, network_node))

    # Write the graph to a file
    graph.write(filename + '.png', format='png')

    # Save the diagram in a static folder
    os.makedirs('static/diagrams', exist_ok=True)
    os.rename(filename + '.png', 'static/diagrams/' + filename + '.png')

    # Render the results page
    return render_template('results.html', project_id=project_id, filename=filename)

# Run the application
if __name__ == '__main__':
    app.run()
