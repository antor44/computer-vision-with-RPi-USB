# Compatible codes of Coursera course "Computer Vision with Embedded Machine Learning" for USB cameras

I don't have a Raspberry Pi to test the course codes due to lack of stock and high prices, so I tried virtualizing the Raspberry Pi Desktop OS and connecting inexpensive Raspberry Pi compatible USB cameras.

## Initial Approach: Raspberry Pi Desktop OS (32-bit)

This is the Raspberry Pi desktop operating system used:
https://www.raspberrypi.com/software/raspberry-pi-desktop/

It is a **32-bit** or **i386** system, **NOT ARM**. It will install with a 64-bit kernel if the chosen processor is 64-bit. Raspberry Pi Desktop seems very compatible with the original Raspberry Pi. To avoid compatibility issues with programs compiled from source, I first chose a 32-bit processor (or `qemu32`) for the virtual machine.

### Virtualization Tests (VirtualBox vs. Qemu/KVM)

I have tried to install this Linux in **VirtualBox** and in **Qemu/KVM**.

1.  **VirtualBox:** The USB cameras do not work as well as in Qemu. In addition, a command is necessary for the cameras connected to a virtual machine. For example, with this command in Linux for the first webcam (`.1`):
    ```bash
    VBoxManage controlvm "Raspberry Pi Desktop" webcam attach .1
    ```

2.  **Qemu/KVM:** This step is not necessary, and it works much better with more resolution options, although at low FPS (15 fps). It will surely work even better with IOMMU or hardware passthrough.

### Hardware Compatibility Notes

Some of the cameras I've tried:
*   **Standard Camera:** https://es.aliexpress.com/item/1005003279752689.html
*   **Cheap camera with Zoom:** https://es.aliexpress.com/item/1005003615538865.html

**Using Mobile Cameras (DroidCam):**
It is also possible to use mobile cameras with **DroidCam**. In VirtualBox with Raspberry Pi Desktop, it recognizes it the same as if it were a USB webcam and it works very well with the high quality of the mobile camera, both by ADB and by Wi-Fi (although much better by ADB).

https://www.dev47apps.com/droidcam/linux/

While it must be installed from source, I seem to recall that—at least for the optional GUI application—DroidCam is not compatible with the 64-bit AMD64 kernel on a 32-bit Linux system.

### Limitations of this Approach

Apart from the DroidCam issue, I also encountered problems with the **Edge Impulse** software; it is not compatible with the 32-bit kernel nor the 64-bit AMD64 kernel on a 32-bit Linux system.

**Summary of the 32-bit attempt:**
The tests were satisfactory for the first two codes of the course, modified for USB cameras, but **not for the following ones** due to the incompatibility of the Edge Impulse software with Linux i386 32-bit (although it is compatible with ARM 32-bit and 64-bit).

---

## The Recommended Solution: Debian 11 (64-bit)

Raspberry Pi Desktop is actually an exact copy of the **Debian 11 (Bullseye)** operating system; its repositories are all official Debian ones. It is then possible to install a **64-bit Debian system with the LXDE desktop**. They are not aesthetically identical, but the most important thing is to preserve similarity in the versions of the libraries between the virtualized system and an original RPi 4.

**Download ISO:** `debian-live-11.4.0-amd64-lxde.iso` from here:
https://www.debian.org/CD/live/

On a PC with **64-bit Linux**, there is no problem running Edge Impulse and the modified Python codes. The programs work on any AMD64 64-bit Linux, be it virtualized or bare metal, as long as the codes are modified for Linux-compatible USB cameras.

### Alternative Method (Not Recommended)

An alternative to installing Debian 64-bit is to try to change the entire system to the AMD64 architecture from a 32-bit Raspberry Pi Desktop installation ("Cross-Grading"). To try this option, it would only be necessary to change the virtualizer configuration to a 64-bit processor.

But several problems are to be expected due to some Raspberry modifications that will not be available in 64-bit, and furthermore, this option does not seem necessary as they are two identical operating systems.
https://wiki.debian.org/CrossGrading

---

## Helpful Resources

**Virtualization with Qemu/KVM:**
*   Copy/Paste from host: https://askubuntu.com/questions/858649/how-can-i-copypaste-from-the-host-to-a-kvm-guest
*   Shared Folders: https://ostechnix.com/setup-a-shared-folder-between-kvm-host-and-guest
*   Mounting Issues: https://superuser.com/questions/502205/libvirt-9p-kvm-mount-in-fstab-fails-to-mount-at-boot-time

**Compatible Sample Codes:**
Compatible sample codes for USB cameras on Linux 64-bit or Raspberry Pi ARM:
https://github.com/antor44/computer-vision-with-RPi-USB

---

## Screenshots

### pi_cam_preview_usb.py:

![pi_cam_preview_usb.py](https://github.com/antor44/computer-vision-with-RPi-USB/blob/main/pi_cam_preview_usb.jpg)

### pi_cam_capture_usb.py:

![pi_cam_capture_usb.py](https://github.com/antor44/computer-vision-with-RPi-USB/blob/main/pi_cam_capture_usb.jpg)

### An image captured:

![An image captured](https://github.com/antor44/computer-vision-with-RPi-USB/blob/main/6.png)

Image cropped and resized to configured sizes. Rotation is also available.

### dnn-live-inference-pi-cam_usb.py:

![dnn-live-inference-pi-cam_usb.py](https://github.com/antor44/computer-vision-with-RPi-USB/blob/main/dnn-live-inference-pi-cam_usb.jpg)

`dnn-live-inference-pi-cam_usb.py` on a virtualized Debian 11 LXDE AMD64.

### dnn-live-colorspace_usb.py:

![dnn-live-colorspace_usb.py](https://github.com/antor44/computer-vision-with-RPi-USB/blob/main/dnn-live-colorspace_usb.jpg)

`dnn-live-colorspace_usb.py` to check if the color space of captured images is BGR. The codes for the Raspberry Pi camera module are for BGR color space and color order, just like these codes for USB cameras, due to the OpenCV library works in BGR color order when images are in color. In the image above, the first pixel (red) is processed correctly: `[x x 255]` (BGR).
