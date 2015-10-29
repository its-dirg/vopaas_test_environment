__author__ = 'haho0032'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from saml2.cert import OpenSSLWrapper

__author__ = 'haho0032'


cert_info_ca = {
    "cn": "test",
    "country_code": "SE",
    "state": "AU",
    "city": "Umea",
    "organization": "ICT",
    "organization_unit": "DIRG"
}

osw = OpenSSLWrapper()
cert_info_ca["cn"] = "op"
ca_cert, ca_key = osw.create_certificate(cert_info_ca, request=False, write_to_file=True,
                                                cert_dir="./", sn=2)

cert_info_ca["cn"] = "proxy_backend"
osw.create_certificate(cert_info_ca, request=False, write_to_file=True,
                                                cert_dir="./", sn=3)

cert_info_ca["cn"] = "proxy_frontend"
osw.create_certificate(cert_info_ca, request=False, write_to_file=True,
                                                cert_dir="./", sn=4)

cert_info_ca["cn"] = "proxy_server"
osw.create_certificate(cert_info_ca, request=False, write_to_file=True,
                                                cert_dir="./", sn=5)
