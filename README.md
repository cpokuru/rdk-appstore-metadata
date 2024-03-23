# rdk-appstore-metadata
curl -X POST   http://127.0.0.1:5000/maintainers   -H 'Content-Type: application/json'   -d '{
          "code": "rdk",
           "name": "rdkm",
           "address": "1800 Arch street Philadelphia PA 19018",
          "homepage": "https://www.rdkcentral.com",
          "email": "chandrakanth_pokuru2@comcast.com"
     }'


 curl -X GET   http://127.0.0.1:5000/maintainers/rdk


 curl -X POST \
  http://127.0.0.1:5000/maintainers/rdk/apps \
  -H 'Content-Type: application/json' \
  -d '{
        "header": {
            "id": "demo.id.rdk5",
            "version": "1.5",
            "icon": "http://rdk.url/rdk5.png",
            "name": "RDK1",
            "description": "Description of rdk5",
            "url": "http://url/rdk5",
            "visible": true,
            "encryption": false,
            "preferred": false,
            "ociImageUrl": "myregistry.local:5000/testing/rdk5",
            "latest" : true,
            "type": "rdk_apps",
            "category": "application",
            "size": "10000000",
            "localization": [
                {
                    "languageCode": "en",
                    "name": "rdk application",
                    "description": "description"
                }
            ]
        },
        "requirements": {
            "dependencies": [
                {
                    "id": "1.5.0",
                    "version": "string"
                }
            ],
            "platform": {
                "architecture": "arm",
                "variant": "v1",
                "os": "linux"
            },
            "hardware": {
                "ram": "string",
                "dmips": "string",
                "persistent": "string",
                "cache": "string"
            },
            "features": [
                {
                    "name": "string",
                    "version": "string",
                    "required": true
                }
            ]
        },
        "maintainer": {
            "name": "rdkm",
            "address": "address",
            "homepage": "http://rdkcentral",
            "email": "chandra@mail.org"
        }
    }'



etadata$ curl -X GET   http://127.0.0.1:5000/maintainers/rdk/apps
[
  {
    "header": "{'id': 'demo.id.appl', 'version': '2.2', 'icon': 'http://pretty.url/icon3.png', 'name': 'FancyApp', 'description': 'Description of Fancy application', 'url': 'http://url/fancyappl', 'visible': True, 'encryption': False, 'preferred': False, 'ociImageUrl': 'myregistry.local:5000/testing/test-image', 'latest': True, 'type': 'fancy_applications', 'category': 'application', 'size': '10000000', 'localization': [{'languageCode': 'en', 'name': 'Fancy application', 'description': 'description'}]}",
    "requirements": "{'dependencies': [{'id': '1.2.3', 'version': 'string'}], 'platform': {'architecture': 'arm', 'variant': 'v1', 'os': 'linux'}, 'hardware': {'ram': 'string', 'dmips': 'string', 'persistent': 'string', 'cache': 'string'}, 'features': [{'name': 'string', 'version': 'string', 'required': True}]}"
  },
  {
    "header": "{'id': 'demo.id.rdk1', 'version': '1.0', 'icon': 'http://rdk.url/icon3.png', 'name': 'FancyApp1', 'description': 'Description of Fancy application1', 'url': 'http://url/fancyappl1', 'visible': True, 'encryption': False, 'preferred': False, 'ociImageUrl': 'myregistry.local:5000/testing/test-image1', 'latest': True, 'type': 'fancy_applications', 'category': 'application', 'size': '10000000', 'localization': [{'languageCode': 'en', 'name': 'Fancy application', 'description': 'description'}]}",
    "requirements": "{'dependencies': [{'id': '1.0.0', 'version': 'string'}], 'platform': {'architecture': 'arm', 'variant': 'v1', 'os': 'linux'}, 'hardware': {'ram': 'string', 'dmips': 'string', 'persistent': 'string', 'cache': 'string'}, 'features': [{'name': 'string', 'version': 'string', 'required': True}]}"
  },
  {
    "header": "{'id': 'demo.id.rdk2', 'version': '1.2', 'icon': 'http://rdk.url/icon3.png', 'name': 'FancyApp1', 'description': 'Description of Fancy application2', 'url': 'http://url/fancyappl2', 'visible': True, 'encryption': False, 'preferred': False, 'ociImageUrl': 'myregistry.local:5000/testing/test-image2', 'latest': True, 'type': 'fancy_applications', 'category': 'application', 'size': '10000000', 'localization': [{'languageCode': 'en', 'name': 'Fancy application', 'description': 'description'}]}",
    "requirements": "{'dependencies': [{'id': '1.2.0', 'version': 'string'}], 'platform': {'architecture': 'arm', 'variant': 'v1', 'os': 'linux'}, 'hardware': {'ram': 'string', 'dmips': 'string', 'persistent': 'string', 'cache': 'string'}, 'features': [{'name': 'string', 'version': 'string', 'required': True}]}"
  },
  {
    "header": "{'id': 'demo.id.rdk3', 'version': '1.3', 'icon': 'http://rdk.url/icon3.png', 'name': 'FancyApp1', 'description': 'Description of Fancy application3', 'url': 'http://url/fancyappl3', 'visible': True, 'encryption': False, 'preferred': False, 'ociImageUrl': 'myregistry.local:5000/testing/test-image3', 'latest': True, 'type': 'fancy_applications', 'category': 'application', 'size': '10000000', 'localization': [{'languageCode': 'en', 'name': 'Fancy application', 'description': 'description'}]}",
    "requirements": "{'dependencies': [{'id': '1.3.0', 'version': 'string'}], 'platform': {'architecture': 'arm', 'variant': 'v1', 'os': 'linux'}, 'hardware': {'ram': 'string', 'dmips': 'string', 'persistent': 'string', 'cache': 'string'}, 'features': [{'name': 'string', 'version': 'string', 'required': True}]}"
  },
  {
    "header": "{'id': 'demo.id.rdk4', 'version': '1.4', 'icon': 'http://rdk.url/rdk1.png', 'name': 'RDK1', 'description': 'Description of rdk1', 'url': 'http://url/rdk1', 'visible': True, 'encryption': False, 'preferred': False, 'ociImageUrl': 'myregistry.local:5000/testing/rdk1', 'latest': True, 'type': 'rdk_apps', 'category': 'application', 'size': '10000000', 'localization': [{'languageCode': 'en', 'name': 'rdk application', 'description': 'description'}]}",
    "requirements": "{'dependencies': [{'id': '1.4.0', 'version': 'string'}], 'platform': {'architecture': 'arm', 'variant': 'v1', 'os': 'linux'}, 'hardware': {'ram': 'string', 'dmips': 'string', 'persistent': 'string', 'cache': 'string'}, 'features': [{'name': 'string', 'version': 'string', 'required': True}]}"
  },
  {
    "header": "{'id': 'demo.id.rdk5', 'version': '1.5', 'icon': 'http://rdk.url/rdk5.png', 'name': 'RDK1', 'description': 'Description of rdk5', 'url': 'http://url/rdk5', 'visible': True, 'encryption': False, 'preferred': False, 'ociImageUrl': 'myregistry.local:5000/testing/rdk5', 'latest': True, 'type': 'rdk_apps', 'category': 'application', 'size': '10000000', 'localization': [{'languageCode': 'en', 'name': 'rdk application', 'description': 'description'}]}",
    "requirements": "{'dependencies': [{'id': '1.5.0', 'version': 'string'}], 'platform': {'architecture': 'arm', 'variant': 'v1', 'os': 'linux'}, 'hardware': {'ram': 'string', 'dmips': 'string', 'persistent': 'string', 'cache': 'string'}, 'features': [{'name': 'string', 'version': 'string', 'required': True}]}"
  }
]
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ 
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ 
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ curl -X GET   http://127.0.0.1:5000/maintainers/rdk/apps/1
{
  "header": "{'id': 'demo.id.appl', 'version': '2.2', 'icon': 'http://pretty.url/icon3.png', 'name': 'FancyApp', 'description': 'Description of Fancy application', 'url': 'http://url/fancyappl', 'visible': True, 'encryption': False, 'preferred': False, 'ociImageUrl': 'myregistry.local:5000/testing/test-image', 'latest': True, 'type': 'fancy_applications', 'category': 'application', 'size': '10000000', 'localization': [{'languageCode': 'en', 'name': 'Fancy application', 'description': 'description'}]}",
  "requirements": "{'dependencies': [{'id': '1.2.3', 'version': 'string'}], 'platform': {'architecture': 'arm', 'variant': 'v1', 'os': 'linux'}, 'hardware': {'ram': 'string', 'dmips': 'string', 'persistent': 'string', 'cache': 'string'}, 'features': [{'name': 'string', 'version': 'string', 'required': True}]}"
}
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ 
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ 
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ 
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ 
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ curl -X GET   http://127.0.0.1:5000/maintainers/rdk
{
  "address": "1800 Arch street Philadelphia PA 19018",
  "code": "rdk",
  "email": "chandrakanth_pokuru2@comcast.com",
  "homepage": "https://www.rdkcentral.com",
  "name": "rdkm"
}
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ 
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ curl -X GET   http://127.0.0.1:5000/maintainers
[
  
  {
    "address": "1800 Arch street Philadelphia PA 19018",
    "code": "rdk",
    "email": "chandrakanth_pokuru2@comcast.com",
    "homepage": "https://www.rdkcentral.com",
    "name": "rdkm"
  }
]
rdkm@RDKM-COMMON:~/ckp/dacwh/newmd/rdk-appstore-metadata/github/rdk-appstore-metadata$ 

 
