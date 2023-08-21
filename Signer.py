#!/usr/bin/python3

# Author: Lord Guccif3r
# Website: www.offensive-paradise.com
# Mail: Guccif3r@offensive.com
# Twitter: @LordGuccif3r

import subprocess
import sys
import os
import random
import string
import argparse
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta

def generate_cert(domain):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    private_key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    public_key = key.public_key()
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, domain),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, domain),
    ]))
    builder = builder.not_valid_before(datetime.utcnow() - timedelta(days=1))
    builder = builder.not_valid_after(datetime.utcnow() + timedelta(days=365))
    builder = builder.serial_number(random.randint(1, 2**64 - 1))
    builder = builder.public_key(public_key)
    cert = builder.sign(private_key=key, algorithm=hashes.SHA256(), backend=default_backend())

    cert_pem = cert.public_bytes(serialization.Encoding.PEM)

    with open(f"{domain}.pem", "wb") as pem_file:
        pem_file.write(cert_pem)

    with open(f"{domain}.key", "w") as key_file:
        key_file.write(private_key_pem)

def generate_pfx(password, domain):
    subprocess.run([
        "openssl", "pkcs12", "-export",
        "-out", f"{domain}.pfx",
        "-inkey", f"{domain}.key",
        "-in", f"{domain}.pem",
        "-passin", f"pass:{password}",
        "-passout", f"pass:{password}"
    ], check=True)

def sign_executable(password, pfx, filein, fileout):
    subprocess.run([
        "osslsigncode", "sign",
        "-pkcs12", pfx,
        "-in", filein,
        "-out", fileout,
        "-pass", password
    ], check=True)


def verify(check):
    try:
        subprocess.run(["osslsigncode", "verify", check], check=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass

def main():
    print("""

                      ███████╗██╗ ██████╗ ███╗   ██╗███████╗██████╗ 
                      ██╔════╝██║██╔════╝ ████╗  ██║██╔════╝██╔══██╗
                      ███████╗██║██║  ███╗██╔██╗ ██║█████╗  ██████╔╝
                      ╚════██║██║██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗
                      ███████║██║╚██████╔╝██║ ╚████║███████╗██║  ██║
                      ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                            
                                        
                                     By Lord Guccif3r
                                        VERSION 2.0
                                              
    """)

    parser = argparse.ArgumentParser(description="Sign and verify executable files")
    parser.add_argument("-i", "--input", help="Input file to be signed")
    parser.add_argument("-d", "--domain", help="Domain to use for signing")
    parser.add_argument("-o", "--out", help="Signed output file")
    parser.add_argument("-v", "--verify", help="Verify if a file is signed")
    parser.add_argument("-p", "--pass", dest="password", help="Password for pfx file")
    parser.add_argument("-x", "--pfx", help="Path to pfx file")
    args = parser.parse_args()

    if not any(vars(args).values()):
        print("No valid arguments provided. Please use -h or --help for usage information.")
        return
    
    if args.verify:
        print(f"[*] Checking code signed on file: {args.verify}")
        verify(args.verify)
        sys.exit(3)

    if args.pfx:
        if not args.input or not args.out or not args.password:
            print("Please provide -i, -o, and -p when signing with a PFX file.")
            return
        print(f"[*] Signing {args.input} with a valid cert {args.pfx}")
        sign_executable(args.password, args.pfx, args.input, args.out)
        print("[+] Signed File Created.")
    else:
        if not args.domain or not args.input or not args.out:
            print("Please provide -i, -d, and -o when signing with a fake cert.")
            return
        password = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
        pfx_file = f"{args.domain}.pfx"
        print(f"[*] Signing {args.input} with a fake cert")
        generate_cert(args.domain)
        generate_pfx(password, args.domain)
        sign_executable(password, pfx_file, args.input, args.out)
        print("[*] Cleaning up....")
        os.remove(f"{args.domain}.pem")
        os.remove(f"{args.domain}.key")
        os.remove(f"{args.domain}.pfx")
        print("[+] Signed File Created.")

if __name__ == "__main__":
    main()
    
