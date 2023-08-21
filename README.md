# Tools developed to sign executables.
## Screenshot of help menu:
![1](https://github.com/LordGuccif3r/Signer/blob/main/Screenshots/1.png)

## Screenshot of signing:
![2](https://github.com/LordGuccif3r/Signer/blob/main/Screenshots/2.png)

## Screenshot of verify:
![3](https://github.com/LordGuccif3r/Signer/blob/main/Screenshots/3.png)


## Requirements and installation 

**DEBIANBASE (kali, parrot) or UBUNTU)**
```
sudo apt-get install osslsigncode
git clone https://github.com/LordGuccif3r/Signer.git
cd Signer
chmod +x signer.py
python Signer.py -h
```
**ARCH LINUX)** 
```
sudo pacman -S osslsigncode
git clone https://github.com/LordGuccif3r/Signer.git
cd Signer
chmod +x signer.py
python Signer.py -h

```

**EXAMPLE OF USE**

# Use -h to get the help 
- python Signer.py -h

# Verify if the executable is signed
- python Signer.py -v malware.exe 

# To sign an executable
- python Signer.py -i malware.exe -d www.mydomain.com -o signed_malware.exe

## Credits

- This tools was develped fallowing the example of https://github.com/Tylous/Limelighter 
