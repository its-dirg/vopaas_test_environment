VOPaaS is a light weight proxy used as a bridge between a SAML2int Service Provider and a number of 
identity providers such as Facebook, google and SAML2int based IdP's.

# Architectural overview

![](images/VOPaaS_overview.png "VOPaaS overview image")

1. The client SP sents a request  
1. The proxy connects to the requested identity provider and receives user infomation 
1. The proxy connects to a account linking service 
1. The proxy connects to a consent manager service 
1. The returned user info attributes which where returned from the 
service provider and for which the user has given consent will be sent to the SP


![](images/VOPaaS_proxy_internals.png "VOPaaS internal communication")

1. Service provider makes request to proxy. At a specific url which specifies which identity it want to use
1. The frontend module is responsible to convert to incoming request to the internal representation 
1. The internal request is passed on the the router
1. The internal request is routed to the right backend based on the url to which the Service provider sent the request
1. The backend converts the request from internal data to external request 
1. The backend send the request and receives user info
1. The backend converts the external response to internal data
1. Then the information is passed on to the account linking module 
1. The account linking module contacts the account linking service by a REST API
1. The information is then passed on to the consent manager
1. The consent manager contacts the consent manager service 
1. The info is passed on to the router 
1. By using a state object the router can determine which frontend module should receive the response
1. The internal data is the converted to a SAML2 int response.
1. The response is returned to the service provider 

![](images/vopaas_consent_comunication.png "VOPaaS internal communication")

1. Verifies if consent was given for a given SP, IdP and set of attributes

    1.1 If no consent where given the requested attributes, a redirect URL and some information 
    about the Service provider will be stored and a ticket will be generated
    
    1.2 Send ticket to show consent page
1. If consent where given the consent service will redirect back to the proxy 


![](images/vopaas_AL_comunication.png "VOPaaS internal communication")

1. Request unique identifier for a given user in combination with a identity provider
    1. If a link between the user and identity provider does NOT exists a ticket is returned to the proxy
        1. Create link between the user and identity provider
        1. Restart flow
    1. If a link between the user and identity provider exists an UUID is returned

# Installation

1. Download this repository as a [zip file](https://github.com/its-dirg/vopaas_ansible/archive/master.zip).
1. All configuration files are located in **TODO add skeleton configuration files somewhere in vopaas_ansible**
1. Modify all necessary parameters, described in [Configuration](configuration).
1. Run `ansible-playbook` **TODO specify command to run and describe example inventory?**
1. **TODO Should SP's/backing IdP's read metadata from URL? (in that case we really should let a proper webserver (nginx or Apache) serve static files).
1. **TODO specify location of generated frontend/backend metadata or make location configurable in Ansible**


# Configuration

In this section all necessary configuration is described.

## Proxy configuration

| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `HOST` | string | `127.0.0.1` | hostname or IP address |
| `PORT` | int | `8080` | port number |
| `HTTPS` | bool | `No` | whether the proxy should use HTTPS |
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
**TODO add path of example/default config file**

#### IdP configuration

**TODO how should SP metadata be handled in production? can VOPaaS reload the specified metadata file at certain intervals or should we use MDX or something else?, see `metadata` param in table below**

**TODO should there be any default "attribute_restrictions"?**
**TODO is the default assertion lifetime reasonable?**
**TODO document contact information (organization, tech support, etc?) in configuration**

Keys in the `config["idp_config"]` necessary to customize:

| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `key_file` | string | `pki/frontend.key` | path to private key used for signing the SAML2 assertions |
| `cert_file` | string | `pki/frontend.crt` | path to certificate for the public key associated with the private key in `key_file` |
| `metadata["local"]` | string[] | `[metadata/sp.xml]` | list of paths to metadata for all service providers connecting to the proxy |
| `state_id` | string | `my_saml_frontend` | key for saving/retrieving data from state dict. Need to be unique per frontend/backend |

## Backend configuration

Two backend plugins are bundled with the VOPaaS proxy:
  * SAML2 backend, making the proxy act as a SAML2 SP communicating with SAML2 IdP's.
  * OpenID Connect backend, making the proxy act as a OpenID Connect Relying Party (RP) communicating with OpenID Connect Providers (OP).


### SAML2 backend

**TODO how should IdP metadata be handled in production? can VOPaaS reload the specified metadata file at certain intervals or should we use MDX or something else?, see `metadata` param in table below**



SP configuration in `config[”config"]` necessary to customize:

| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `organization` | dict | `{display_name: Example Identities, name: Example Identities Organization, url: https://www.example.com}` | information about the organization, will be published in the SAML metadata |
| `contact_person` | dict[] | `{contact_type: technical, given_name: Someone Technical, email_address: technical@example.com}` | list of contact information, will be published in the SAML metadata |
| `key_file` | string | `pki/backend.key` | path to private key used for signing the SAML authentication requests |
| `cert_file` | string | `pki/backend.crt` | path to certificate for the public key associated with the private key in `key_file` |
| `metadata["local"]` | string[] | `[metadata/idp.xml]` | list of paths to metadata for all backing IdP's |
| `state_id` | string | `my_saml_backend` | key for saving/retrieving data from state dict. Need to be unique per frontend/backend |


### Social login backends

#### Google
| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `client_registration["client_id"]` | string | `abcdefgh` | client ID designated by Google |
| `client_registration["client_secret"]` | string | `123456` | client secret designated by Google |
| `state_id` | | | **TODO (same as `state_key` in FB plugin)?** |

#### Facebook

| Parameter name | Data type | Example value | Description |
| -------------- | --------- | ------------- | ----------- |
| `client_config["client_id"]` | string | `123456789` | "App ID" designated by Facebook |
| `client_secret` | string | `a1b2c3d4e5` | "App Secret" designated by Facebook |
| `state_key` | | | **TODO?** |

**TODO set sane defaults for `fields` in vopaas example/default FB config**

# Service Provider requirements

* Technical requirement: Any SP connecting to the proxy must provide an `mdui:DisplayName` in the metadata. **TODO can we expect this or should we have a fallback when fetching the `requester_name` to send to the consent service?**
