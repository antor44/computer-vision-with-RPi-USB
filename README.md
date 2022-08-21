# Compatible codes of Coursera course Computer Vision with Embedded Machine Learning for USB cameras and virtual machines

I don't have a Raspberry Pi to test the course codes due to lack of stock and high prices, so I tried virtualizing the Raspberry Pi desktop OS and connecting inexpensive Raspberry Pi compatible USB cameras. The tests were satisfactory for the first two codes of the course, modified for USB cameras, but not for the following ones due to the incompatibility of Edge Impulse software with linux i386 or Intel 32 bit, it is compatible with arm 32 bits.

This is the Raspberry Pi desktop operating system:

https://www.raspberrypi.com/software/raspberry-pi-desktop/

Although it is a 32-bit system or i386, not ARM, it can be installed with a 64-bit kernel from the official repositories, but to avoid compatibility problems with programs compiled from source it is a good idea to choose a 32-bit processor or the qemu32 for the virtual machine. Raspberry Pi Desktop seems very compatible with the original Raspberry Pi, I have tried installing this linux in VirtualBox and in Qemu/KVM. In VirtualBox the USB cameras do not work as well as in Qemu, in addition, in addition a command is necessary for the cameras connected to a virtual machine, for example with this command in linux for the first webcam (.1):

VBoxManage controlvm "Raspberry Pi Desktop" webcam attach .1

In Qemu/KVM this step is not necessary and it works much better, with more resolution options although at low fps (15 fps), it will surely work even better with IOMMU or hardware passthrough.

Some of the cameras I've tried:

https://es.aliexpress.com/item/1005003279752689.html

With Zoom:

https://es.aliexpress.com/item/1005003615538865.html

It is also possible to use the mobile cameras with DroidCam, in VirtualBox with Raspberry Pi Desktop it recognizes it the same as if it were a USB webcam and it works very well, with the quality of the mobile camera, both by ADB and by Wifi, although much better by ADB. While it needs to be installed from source, I seem to recall that at least for the optional GUI application it is not compatible with 64-bit amd64 kernel on a 32-bit linux system.

Ultimately, I have not been able to run the programs on a virtualized Raspberry Pi Desktop system, although they would work on any 64-bit linux, be it virtualized or bare metal, as long as the codes are modified for linux compatible USB cameras.

Compatible codes for USB cameras on linux 64 bits or Raspberry PI arm:

https://github.com/antor44/computer-vision-with-RPi-USB

---

## pi_cam_preview_usb.py:

![pi_cam_preview_usb.py](https://github.com/antor44/computer-vision-with-RPi-USB/blob/main/pi_cam_preview_usb.jpg)

## pi_cam_capture_usb.py:

![pi_cam_capture_usb.py](https://github.com/antor44/computer-vision-with-RPi-USB/blob/main/pi_cam_capture_usb.jpg)

## An image captured:

![An image captured](https://github.com/antor44/computer-vision-with-RPi-USB/blob/main/6.png)

Image cropped and resized to configured sizes. Rotation is also available.
