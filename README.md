# Compatible codes of Coursera course Computer Vision with Embedded Machine Learning for USB cameras and virtual machines

I don't have a Raspberry Pi to test the course codes due to lack of stock and high prices, so I tried virtualizing the Raspberry Pi Desktop OS and connecting inexpensive Raspberry Pi compatible USB cameras. The tests are satisfactory for the first two modified codes of the course, I have not yet advanced further.

This is the Raspberry Pi Desktop OS:

https://www.raspberrypi.com/software/raspberry-pi-desktop/

Although it is a 32-bit 686 system, not ARM, it seems very compatible with the original Raspberry Pi. I have installed it on linux in VirtualBox and in Qemu/KVM. In VirtualBox the USB cameras do not work as well as in Qemu, in addition, a for the camera to a virtual machine is necessary, for example with this command in linux for the first webcam (.1):

VBoxManage controlvm "Raspberry Pi Desktop" webcam attach .1

In Qemu/KVM it is not necessary and it works much better, with more resolution options although at low fps, it will surely work even better with IOMMU or passthrough.

Some of the cameras I've tried:

https://es.aliexpress.com/item/1005003279752689.html

With Zoom:

https://es.aliexpress.com/item/1005003615538865.html

It is also possible to use the mobile with DroidCam, in VirtualBox with Raspberry Pi Desktop it recognizes it as a USB device and it works very well, both by ADB and by Wifi, although I think I remember that it is necessary to install it from the source.

