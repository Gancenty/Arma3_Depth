import open3d as o3d
import numpy as np
import cv2
import time

# Load the point cloud file
pcd = o3d.io.read_point_cloud("Filted\[8500-18200].ply")

# Initialize the Open3D visualizer
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(pcd)

# Run a loop to update the depth map as the camera changes
try:
    while True:
        # Capture the depth image from the current camera view
        depth = vis.capture_depth_float_buffer(True)
        depth_image = np.asarray(depth)

        # Normalize depth image for display with OpenCV
        depth_normalized = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Display the depth map using OpenCV
        cv2.imshow("Depth Map from Point Cloud", depth_normalized)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Allow Open3D to update the visualization and handle user inputs
        vis.poll_events()
        vis.update_renderer()

except KeyboardInterrupt:
    print("Closing visualization...")

finally:
    # Clean up Open3D and OpenCV windows
    vis.destroy_window()
    cv2.destroyAllWindows()