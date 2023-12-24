#!/bin/sh
echo "
Verifying root permsisions...
"

if [ "$(id -u)" -ne 0 ]; then

echo "
Superuser permissions verification failed, please execute this script with root permissions.
Halting script...
"
  exit 1

fi

echo "
Verifying the existence of plymouth...
"

if pacman -Qi plymouth &> /dev/null; then

  echo "
Plymouth found!
"

else
  echo "
Plymouth is not installed, Here you can install it: https://wiki.archlinux.org/title/Plymouth 
Halting script...
"
 exit 1
fi

echo "
Verifying the existence of the compressed tar file included in the download of the theme...
"

theme-file="./spinner-endeavouros.tar"

if [ -e "$theme-file" ]; then

echo "
Theme compressed file in place! 

Verification steps finished, proceeding to the installation...
"

else

echo "
The compressed theme file (spinner-endeavouros.tar) is misplaced or it doesn't exist... Please verify the existence of the compressed file and place it in the same directory of this script...
"
exit 1

fi

echo "
Extracting theme into Plymouth themes...
"

tar --extract -f spinner-endeavouros.tar --directory=/usr/share/plymouth/themes/

echo "
Changing the default theme
"

plymouth-set-default-theme spinner-endeavouros

echo "
Regenerating initramfs...
"

mkinitcpio="/bin/mkinitcpio"
dracut="/bin/dracut"

if [ -e "$mkinitcpio" ]; then

echo "
Regenerating initramfs with mkinitcpio...
"

mkinitcpio -P

echo "
Done! You have to reboot to apply the theme.
"

elif [ -e "$dracut" ]; then

echo "
Regenerating initramfs with dracut...
"

dracut -f

echo "
Done! You have to reboot to apply the theme.
"

else

echo "
Done! But you don't have either mkinitcpio or dracut, please, regenerate your initramfs manually to apply the theme in early boot.
"

fi