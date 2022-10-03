#!/usr/bin/env python
"""
Pi Camera Static Image Classification

Detects objects in continuous stream of images from Pi Camera. Use Edge Impulse
Runner and downloaded .eim model file to perform inference. Bounding box info is
drawn on top of detected objects along with framerate (FPS) in top-left corner.

Copy one of the test images to the same folder, rename image_file as necessary
(e.g. "48.png").

Author: EdgeImpulse, Inc.
Date: August 3, 2021
License: Apache-2.0 (apache.org/licenses/LICENSE-2.0)
"""

import os, sys, time
from edge_impulse_linux.runner import ImpulseRunner

# Settings

model_file = "modelfile.eim"            # Trained ML model from Edge Impulse


# Copy in features

features = [0.5930, 0.5961, 0.5961, 0.6000, 0.6008, 0.6078, 0.6078, 0.6118, 0.6118, 0.6118, 0.6137, 0.6157, 0.6157, 0.6196, 0.6237, 0.6213, 0.6275, 0.6275, 0.6275, 0.6221, 0.6157, 0.6157, 0.6157, 0.6126, 0.6126, 0.6118, 0.6118, 0.6126, 0.5930, 0.5961, 0.6000, 0.6025, 0.6039, 0.6078, 0.6078, 0.6118, 0.6118, 0.6143, 0.6169, 0.6261, 0.6275, 0.6275, 0.6275, 0.6275, 0.6275, 0.6275, 0.6275, 0.6256, 0.6261, 0.6275, 0.6235, 0.6275, 0.6241, 0.6182, 0.6205, 0.6235, 0.5961, 0.6000, 0.6039, 0.6078, 0.6112, 0.6118, 0.6118, 0.6157, 0.6157, 0.6272, 0.6220, 0.6275, 0.6275, 0.6275, 0.6275, 0.6275, 0.6275, 0.6314, 0.6314, 0.6314, 0.6285, 0.6275, 0.6314, 0.6311, 0.6273, 0.6275, 0.6294, 0.6198, 0.5961, 0.6000, 0.6003, 0.6088, 0.6136, 0.6137, 0.6153, 0.6161, 0.6255, 0.6275, 0.6275, 0.6275, 0.6275, 0.6275, 0.6275, 0.6275, 0.6277, 0.6314, 0.6332, 0.6333, 0.6314, 0.6314, 0.6314, 0.6325, 0.5627, 0.5485, 0.6070, 0.6462, 0.6000, 0.6000, 0.6039, 0.6098, 0.6154, 0.6160, 0.6157, 0.6165, 0.6298, 0.6308, 0.6314, 0.6314, 0.6314, 0.6314, 0.6314, 0.6314, 0.6316, 0.6350, 0.6392, 0.6353, 0.6353, 0.6314, 0.6353, 0.4826, 0.4178, 0.5125, 0.4954, 0.4435, 0.6039, 0.6053, 0.6079, 0.6118, 0.6170, 0.6210, 0.6280, 0.6314, 0.6353, 0.6285, 0.6245, 0.6244, 0.6216, 0.6154, 0.6120, 0.6157, 0.6261, 0.6359, 0.6406, 0.6431, 0.6406, 0.6434, 0.5973, 0.3410, 0.3676, 0.4684, 0.4611, 0.4294, 0.6078, 0.6078, 0.6120, 0.6218, 0.6196, 0.6286, 0.6351, 0.5745, 0.4459, 0.3860, 0.3716, 0.3512, 0.3191, 0.3193, 0.3570, 0.3683, 0.3765, 0.3948, 0.4354, 0.5059, 0.5741, 0.5686, 0.4453, 0.3508, 0.2592, 0.2636, 0.2873, 0.3244, 0.6078, 0.6118, 0.6159, 0.6262, 0.6275, 0.6316, 0.5114, 0.3153, 0.3042, 0.3129, 0.3125, 0.3025, 0.2521, 0.2638, 0.3272, 0.3333, 0.3325, 0.3308, 0.3385, 0.3376, 0.3169, 0.4412, 0.4896, 0.3052, 0.4384, 0.5638, 0.6098, 0.6177, 0.6118, 0.6118, 0.6144, 0.6176, 0.6275, 0.5864, 0.3133, 0.2902, 0.2796, 0.2657, 0.2870, 0.2977, 0.2915, 0.2773, 0.3157, 0.3308, 0.3188, 0.3109, 0.3666, 0.4241, 0.4854, 0.4807, 0.3592, 0.3908, 0.5957, 0.6430, 0.6431, 0.6361, 0.6157, 0.6157, 0.6160, 0.6275, 0.6272, 0.4676, 0.2716, 0.2902, 0.2822, 0.2669, 0.2846, 0.2882, 0.2587, 0.2863, 0.2999, 0.3294, 0.3092, 0.2745, 0.3070, 0.3030, 0.2876, 0.2801, 0.3442, 0.5282, 0.6339, 0.6431, 0.6391, 0.6353, 0.6157, 0.6157, 0.6160, 0.6275, 0.6276, 0.3510, 0.2752, 0.2945, 0.2980, 0.2919, 0.2892, 0.3116, 0.2829, 0.2730, 0.3057, 0.3301, 0.3150, 0.2627, 0.3024, 0.3803, 0.4507, 0.5223, 0.5943, 0.6375, 0.6431, 0.6431, 0.6385, 0.6353, 0.6118, 0.6143, 0.6157, 0.6199, 0.6019, 0.3077, 0.2776, 0.2933, 0.2742, 0.2938, 0.2723, 0.3017, 0.2894, 0.2994, 0.3017, 0.3318, 0.3339, 0.4472, 0.5975, 0.6360, 0.6527, 0.6543, 0.6583, 0.6507, 0.6431, 0.6395, 0.6379, 0.6314, 0.6118, 0.6157, 0.6182, 0.6137, 0.5705, 0.2894, 0.2768, 0.2967, 0.2720, 0.3027, 0.2969, 0.3188, 0.3170, 0.3118, 0.3210, 0.3351, 0.3387, 0.5269, 0.6488, 0.6549, 0.6549, 0.6549, 0.6549, 0.6470, 0.6431, 0.6392, 0.6348, 0.6314, 0.6118, 0.6118, 0.6118, 0.6098, 0.5448, 0.2868, 0.2728, 0.2980, 0.2930, 0.3055, 0.3168, 0.3520, 0.2911, 0.2825, 0.2709, 0.3345, 0.3350, 0.5248, 0.6504, 0.6580, 0.6619, 0.6541, 0.6479, 0.6468, 0.6431, 0.6356, 0.6345, 0.6314, 0.6039, 0.6070, 0.6118, 0.6031, 0.5277, 0.2785, 0.2682, 0.2941, 0.3056, 0.2961, 0.5014, 0.6486, 0.5547, 0.5159, 0.3834, 0.3798, 0.3378, 0.4398, 0.6378, 0.6496, 0.6496, 0.6529, 0.6485, 0.6467, 0.6436, 0.6403, 0.6361, 0.6353, 0.6039, 0.6039, 0.6118, 0.5980, 0.5189, 0.2801, 0.2555, 0.2790, 0.2980, 0.3199, 0.3623, 0.4194, 0.4420, 0.4544, 0.3798, 0.3590, 0.3438, 0.3485, 0.4223, 0.4310, 0.3985, 0.4972, 0.5789, 0.5694, 0.5630, 0.6373, 0.6367, 0.6353, 0.6039, 0.6041, 0.6078, 0.5980, 0.5238, 0.3043, 0.2311, 0.2557, 0.2723, 0.2894, 0.2894, 0.2894, 0.2969, 0.2969, 0.3006, 0.3006, 0.3008, 0.3024, 0.3042, 0.3113, 0.3234, 0.3545, 0.3867, 0.3599, 0.2985, 0.4944, 0.6348, 0.6317, 0.6039, 0.6039, 0.6077, 0.5971, 0.5354, 0.3501, 0.2256, 0.2161, 0.2228, 0.2394, 0.2441, 0.2471, 0.2471, 0.2455, 0.2471, 0.2458, 0.2490, 0.2520, 0.3057, 0.4546, 0.4695, 0.4545, 0.4626, 0.4401, 0.2637, 0.3301, 0.5580, 0.6262, 0.6003, 0.6003, 0.6039, 0.6018, 0.5541, 0.3860, 0.2232, 0.2068, 0.2003, 0.2084, 0.2122, 0.2160, 0.2197, 0.2227, 0.2235, 0.2142, 0.1896, 0.1878, 0.2283, 0.2670, 0.2982, 0.3176, 0.2860, 0.2625, 0.3217, 0.3248, 0.5474, 0.6085, 0.5992, 0.6000, 0.6078, 0.6000, 0.5786, 0.4620, 0.2230, 0.1700, 0.1927, 0.1971, 0.2007, 0.2018, 0.1885, 0.1616, 0.1426, 0.1624, 0.2174, 0.3083, 0.4388, 0.5399, 0.5911, 0.6042, 0.5850, 0.4461, 0.3011, 0.3279, 0.3116, 0.3786, 0.5976, 0.6000, 0.6008, 0.6000, 0.5953, 0.5554, 0.4091, 0.2094, 0.1299, 0.1255, 0.1246, 0.1359, 0.1745, 0.2427, 0.3438, 0.4493, 0.5358, 0.5954, 0.6374, 0.6521, 0.6541, 0.6532, 0.6406, 0.6054, 0.4338, 0.2671, 0.2709, 0.2685, 0.5961, 0.5961, 0.5910, 0.5878, 0.5960, 0.5919, 0.5719, 0.4942, 0.4117, 0.3875, 0.4094, 0.4544, 0.5176, 0.5708, 0.6059, 0.6266, 0.6431, 0.6447, 0.6538, 0.6580, 0.6477, 0.6456, 0.6398, 0.6280, 0.5909, 0.4961, 0.3995, 0.3790, 0.5961, 0.5910, 0.5843, 0.5882, 0.5958, 0.5975, 0.6031, 0.6061, 0.5983, 0.6025, 0.6120, 0.6230, 0.6291, 0.6311, 0.6314, 0.6353, 0.6367, 0.6367, 0.6429, 0.6445, 0.6434, 0.6431, 0.6392, 0.6314, 0.6275, 0.6246, 0.6218, 0.6218, 0.5880, 0.5843, 0.5927, 0.5961, 0.5961, 0.5977, 0.6029, 0.6076, 0.6115, 0.6160, 0.6255, 0.6275, 0.6272, 0.6272, 0.6282, 0.6311, 0.6311, 0.6314, 0.6353, 0.6392, 0.6392, 0.6392, 0.6389, 0.6314, 0.6314, 0.6314, 0.6314, 0.6314, 0.5765, 0.5797, 0.5905, 0.5941, 0.5941, 0.5948, 0.5980, 0.6004, 0.6032, 0.6101, 0.6216, 0.6176, 0.6169, 0.6168, 0.6235, 0.6216, 0.6237, 0.6275, 0.6314, 0.6340, 0.6353, 0.6349, 0.6314, 0.6314, 0.6314, 0.6314, 0.6300, 0.6275, 0.5689, 0.5689, 0.5765, 0.5807, 0.5807, 0.5843, 0.5877, 0.5932, 0.5964, 0.6039, 0.6081, 0.6042, 0.6080, 0.6042, 0.6053, 0.6120, 0.6120, 0.6161, 0.6235, 0.6276, 0.6277, 0.6267, 0.6202, 0.6204, 0.6275, 0.6275, 0.6275, 0.6275, 0.5555, 0.5619, 0.5688, 0.5725, 0.5751, 0.5765, 0.5785, 0.5829, 0.5894, 0.5961, 0.5961, 0.5961, 0.5986, 0.5997, 0.6005, 0.6034, 0.6000, 0.6013, 0.6063, 0.6143, 0.6168, 0.6143, 0.6104, 0.6104, 0.6143, 0.6179, 0.6275, 0.6275, 0.5490, 0.5544, 0.5650, 0.5686, 0.5686, 0.5706, 0.5725, 0.5804, 0.5829, 0.5852, 0.5847, 0.5843, 0.5852, 0.5891, 0.5930, 0.5930, 0.5882, 0.5887, 0.5959, 0.6003, 0.6039, 0.6039, 0.6039, 0.6039, 0.6078, 0.6118, 0.6126, 0.6126]



# Print something to the console

print()
print("---Static Features Inference Test---")


# The ImpulseRunner module will attempt to load files relative to its location,
# so we make it load files relative to this program instead
dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(dir_path, model_file)

# Load the model file
runner = ImpulseRunner(model_path)

# Initialize model (and print information if it loads)
try:
    model_info = runner.init()
    print("Model name:", model_info['project']['name'])
    print("Model owner:", model_info['project']['owner'])

    # Perforrm inference and time how long it takes
    start_time = time.time_ns()
    res = runner.classify(features)
    elapsed_time = time.time_ns() - start_time

    
    # Display predictions and timing data
    print("Predictions:")
    predictions = res['result']['classification']
    for p in predictions:
        print("  " + p + ": " + str(predictions[p]))

    # Print out how long it took to perform inference
    print("Inference time:", (elapsed_time / 1000000), "ms")

    # Print out the timing breakdown
    print("Timing breakdown:", res['timing'])
    
# Exit if we cannot initialize the model
except Exception as e:
    print("ERROR: Could not initialize model")
    print("Exception:", e)
    if (runner):
            runner.stop()
    sys.exit(1)
    

finally:
    if (runner):
            runner.stop()
    print()
