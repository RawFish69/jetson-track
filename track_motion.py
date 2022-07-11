#!/usr/bin/env python3
__version__ = '1.0'

from lab.tracking import TrackingCamera

def run_camera():
    """When terminal displays any error or warning, restart jetson manually"""
    # TrackingCamera configurations
    camera_kwargs = {
        'input_source': 0,                    
                                              
        'mode': 'motion',                     
        'output_video': 'data_video.mp4',     
        'output_data': 'data_output.csv',       
        'camera_settings': (1920, 1080, 30),  
        'tracking_config_file': 'stickers',   
                                              
        'marker_names': [],                   
        'crop': True,                         
                                              
        'builtin_plot_mode': 'default',       
                                             
        'camera_distance': 45                

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
