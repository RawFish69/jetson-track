#!/usr/bin/env python3
__version__ = '1.0'

from lab.tracking import TrackingCamera

def run_camera():
    """When terminal displays any error or warning, restart jetson manually"""
    # TrackingCamera configurations
    camera_kwargs = {
        'input_source': 0,                    # camera id, set this to 0 if you want to read live camera data
                                              # or to input_file if you want to read data from a saved mp4 file 
        'mode': 'motion',                     # optional, the camera mode [recording, tracking (default), motion, calibration]
        'output_video': 'lab6_output.mp4',      # optional, save the output video file (`mp4` format only)
        'output_data': 'lab6_output.csv',       # optional, save the tracking data (to `.csv` files)
        'camera_settings': (1920, 1080, 30),  # optional (width, height, fps), (1920, 1080, 30) by default
        'tracking_config_file': 'stickers',   # optional, markers for tracking or motion
                                              #           '<name>' for builtin config or '<name>.config' for local file
        'marker_names': [],                   # optional, selected markers in tracking config (empty for all)
        'crop': True,                         # optional, if True (default) frame is cropped to near square, otherwise the full resolution is used
                                              #           always False for video file input
        'builtin_plot_mode': 'default',       # optional, 'none' for no plotting by lib
                                              #           'default' for plotting center, contour, etc, may add 'trace' for future
        'camera_distance': 45                # optional, camera distance (in cm) to object

    }

    # Create & run TrackingCamera instance.
    with TrackingCamera(**camera_kwargs) as camera:
        while camera.is_running:
        
            # Read tracking data, then display and write out.
            # Returns None values if camera is busy or if read fails.
            motion_frame_no, motion_frame = camera.read_motion()
            camera.write_frame_to_video(motion_frame_no, motion_frame)
            camera.display_frame(motion_frame_no, motion_frame)

            # Print tracking info to the terminal.
            if motion_frame_no is None:
                continue
            if (motion_frame_no % 30 == 0):
                motion_frame_ts = camera.get_timestamp_of_frame(motion_frame_no)
                print("Frame #{}, {:.1f}ms Stickers: ".format(motion_frame_no, motion_frame_ts),end='')
                for marker_name, marker_data in camera.get_tracking_data_of_frame(motion_frame_no):
                    y, x = marker_data["position_pixel"]
                    print(marker_name, "({}, {}),".format(y, x),end = '')
                print("")

            # Print motion information to terminal.
            if motion_frame_no is None:
                continue
            if (motion_frame_no % 30 == 0 and motion_frame_no > 0):
                motion_frame_ts = camera.get_timestamp_of_frame(motion_frame_no)
                print("Frame #{}, {:.1f}ms".format(motion_frame_no, motion_frame_ts))
                # Print velocity and acceleration.
                for marker_name, marker_data in camera.get_motion_data_of_frame(motion_frame_no):
                    print("Marker name: {}".format(marker_name))
                    print("\tv: {}, a: {}".format(marker_data["v"], marker_data["a"]))

if __name__ == "__main__":
    run_camera()
