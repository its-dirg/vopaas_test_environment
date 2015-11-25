# Configuration

In this section all necessary configuration is described.

## Proxy configuration

| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `HOST` | string | `127.0.0.1` | hostname or IP address |
| `PORT` | int | `8080` | port number |
| `HTTPS` | bool (Yes/No) | `No` | whether the proxy should use HTTPS |
| `SERVER_CERT` | string | `/etc/ssl/cert.pem` | path to certificate for HTTPS, optional if `HTTPS: No` | 
| `SERVER_KEY` | string | `/etc/ssl/key.pem` | path to private key for HTTPS cert, optional if `HTTPS: No` | 
| `CERT_CHAIN` | string | `/etc/ssl/chain.pem` | path to certificate chain file for HTTPS cert, optional if `HTTPS: No`, and may be `Null` (for using with self-signed certificates in a development environment) |
| `SESSION_OPTS` | dict | `{session.type: memory, session.cookie_expires: Yes, session.auto: Yes}` | configuration options for [Beaker Session Middleware](http://beaker.readthedocs.org/en/latest/configuration.html)
| `COOKIE_STATE_NAME` | string | `vopaas_state` | name of cooke VOPaaS uses for preserving state between requests |
| `STATE_ENCRYPTION_KEY` | string | `52fddd3528a44157` | key used for encrypting the state cookie |
| `INTERNAL_ATTRIBUTES` | string | `example/internal_attributes.yaml` | path to attribute mapping
| `PLUGIN_PATH` | string[] | `[example/plugins/backends, example/plugins/frontends]` | list of directory paths containing any front-/backend plugins |
| `BACKEND_MODULES` | string[] | `[oidc_backend, saml2_backend]` | list of plugin names to load from the directories in `PLUGIN_PATH` |
| `FRONTEND_MODULES` | string[] | `[saml2_frontend]` | list of plugin names to load from the directories in `PLUGIN_PATH` |
| `USER_ID_HASH_SALT` | string | `61a89d2db0b9e1e2` | salt used when creating the persistent user identifier |
| `CONSENT` | dict | see configuration of [Additional Services](#additional-services) | optional configuration of consent service |
| `ACCOUNT_LINKING` | dict | see configuration of [Additional Services](#additional-services) | optional configuration of account linking service |

### Additional services
| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `enable` | bool | `Yes` | whether the service should be used |
| `rest_uri` | string | `https://localhost` | url to the REST endpoint of the service |
| `redirect` | string | `https://localhost/redirect` | url to the endpoint where the user should be redirected for necessary interaction |
| `endpoint` | string | `handle_consent` | name of the endpoint in VOPaas where the response from the service is received |
| `sign_key`| string | `pki/consent.key` | path to key used for signing the requests to the service |
| `verify_ssl` | bool | `No` | whether the HTTPS certificate of the service should be verified when doing requests to it |

If using the [CMService](https://github.com/its-dirg/CMservice) for consent management and the [ALService](https://github.com/its-dirg/ALservice) for account linking, the `redirect` parameter should be `https://<host>/consent` and `https://<host>/approve` in the respective configuration entry.


## Frontend configuration

One frontend plugin is bundled with the VOPaaS proxy, a SAML2 plugin making the
proxy look as a SAML2 Identity Provider (IdP) accepting authentication requests
from SAML2 Service Providers (SP).

### SAML2 frontend

| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `MODULE` | python module | `VOPaaSSamlFrontend` | python module backing the plugin |
| `RECEIVER` | string | `VOPaaSSamlFrontend` | name of the frontend used as part of the path in the endpoints this frontend publishes |
| `ENDPOINTS` | dict | `{"single_sign_on_service": {saml2.BINDING_HTTP_REDIRECT: "sso/redirect", saml2.BINDING_HTTP_POST: "sso/post"}}` | mapping of SAML2 request binding to url path |

#### IdP configuration

**TODO** how is the final entity id computed/why does it contain seemingly random characters?

**TODO** how should SP metadata be handled in production? can VOPaaS reload the specified metadata file at certain intervals or should we use MDX or something else?, see `metadata` param in table below

**TODO** should there be any default "attribute_restrictions"?
**TODO** is the default assertion lifetime reasonable?
**TODO** contact information (organization, tech support, etc?) in configuration

Keys in the Saml2FrontendModulePlugin().idpConfig necessary to customize:

| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `key_file` | string | `pki/frontend.key` | path to private key used for signing the SAML2 assertions |
| `cert_file` | string | `pki/frontend.crt` | path to certificate for the public key associated with the private key in `key_file`
| `metadata["local"]` | string[] | `["metadata/sp.xml"]` | list of paths to metadata for all service providers connecting to the proxy |
