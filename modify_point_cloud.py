import open3d as o3d
import numpy as np

def load_ply(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    return pcd

def save_ply(pcd, file_path):
    o3d.io.write_point_cloud(file_path, pcd)

def visualize_and_edit(pcd):
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()
    vis.destroy_window()
    return vis.get_picked_points()

def modify_selected_points(pcd, selected_indices, new_color, translation_vector):
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    
    # Modify selected points
    points[selected_indices] += translation_vector
    colors[selected_indices] = new_color
    
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd

# Load the point cloud
input_file = "C:/Users/admin/pinokio/api/gaussian-splatting.git/output/cup/point_cloud/iteration_5000/point_cloud.ply"
pcd = load_ply(input_file)

# Set default color to all points (if not already set)
if not pcd.has_colors():
    colors = np.zeros((len(pcd.points), 3))  # Default to black
    pcd.colors = o3d.utility.Vector3dVector(colors)

# Visualize and select points
selected_indices = visualize_and_edit(pcd)
print(f"Selected point indices: {selected_indices}")

# New color and translation vector for the selected points
new_color = [1, 0, 0]  # Red color
translation_vector = [0.1, 0, 0]  # Move points along the x-axis

# Modify selected points
pcd = modify_selected_points(pcd, selected_indices, new_color, translation_vector)

# Save the modified point cloud
output_file = "C:/Users/admin/pinokio/api/gaussian-splatting.git/output/cup/point_cloud/iteration_5000/modified_point_cloud.ply"
save_ply(pcd, output_file)

# Visualize the result
o3d.visualization.draw_geometries([pcd])


# Save the modified point cloud
output_file = "C:/Users/admin/pinokio/api/gaussian-splatting.git/output/cup/point_cloud/iteration_5000/modified_point_cloud.ply"
save_ply(pcd, output_file)

# Visualize the result
o3d.visualization.draw_geometries([pcd])


