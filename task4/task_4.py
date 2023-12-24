import time

class NestedSetModel:
    def __init__(self):
        # Initialize the tree structure and index variables
        self.tree = []
        self.left_index = 1
        self.right_index = 2

    def convert_to_nested_set(self, hierarchy):
        # Reset tree and index variables before converting
        self.tree = []
        self.left_index = 1
        self.right_index = 2
        # Build the nested set model recursively
        self._build_nested_set(hierarchy)
        return self.tree

    def _build_nested_set(self, hierarchy, depth=0):
        # Recursively traverse the hierarchy and build the nested set=
        print("called")
        for child_id, child_data in hierarchy.items():
            parent_index = len(self.tree)
            
            self.tree.append({
                'id': child_id,
                'left': self.left_index,
                'right': None,
                'depth': depth,
            })
            
            self.left_index += 1
            # Recursively call for children
            self._build_nested_set(child_data, depth + 1)
            # Update the right index after processing children
            self.tree[parent_index]['right'] = self.left_index
            self.left_index += 1

    def get_parent_child_relationships(self):
        # Create a dictionary to store parent-child relationships
        relationships = {}
        for node in self.tree:
            # Determine the parent of each node
            parent_id = None if node['depth'] == 0 else self._find_parent(node)
            relationships[node['id']] = parent_id
        return relationships

    def _find_parent(self, node):
        # Find the parent of a node by checking left and right indexes
        for parent_node in reversed(self.tree[:self.tree.index(node)]):
            if parent_node['depth'] == node['depth'] - 1 and parent_node['left'] < node['left'] and parent_node['right'] > node['right']:
                return parent_node['id']
        return None

def measure_performance(hierarchy):
    start_time = time.time()
    
    nested_set_model = NestedSetModel()
    # Convert hierarchical data to nested set model
    nested_set_model.convert_to_nested_set(hierarchy)
    # Retrieve parent-child relationships
    parent_child_relationships = nested_set_model.get_parent_child_relationships()

    end_time = time.time()
    execution_time = end_time - start_time

    # Display results and performance metrics
    print("Nested Set Model:", nested_set_model.tree)
    print("Parent-Child Relationships:", parent_child_relationships)
    print("Execution Time: {:.6f} seconds".format(execution_time))

# Example data:
hierarchical_data = {
    'A': {
        'A1': {},
        'A2': {
            'A2.1': {},
            'A2.2': {}
        }
    },
    'B': {
        'B1': {},
        'B2': {}
    }
}

measure_performance(hierarchical_data)