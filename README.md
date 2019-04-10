 :exclamation: :boom: It was formerly used as proxy for HydraPlay. Since HydraPlay is compatible with websockify, this project is not maintained anymore. I will leave it here as code sample.  :boom: :exclamation:

# Snapcast Websocket and HTTP Proxy

A small proxy server for routing snapcast api reaquests over websockets and http requests.
This server can be used as middleware between snapcasts raw tcp sockets and a web applications.
It was mainly developed for the usage with the snapcast multiplayer.

## Getting Started

Just install and start the proxy on the same host as your snapcst sever is running. 


### Installing

The server uses python3. Be sure that pyhton3 is installed on your system. 
Install the dependencies with:

```
pip install tornado. 
```

or

```
pip3 install tornado. 
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Mario Lukas** - *Initial work* - [GitHub](https://github.com/mariolukas)

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Performance is slow if it it runs in debug mode, due to all the log outputs

TODO: 
* Performance Tweeks for websocket - telnet communication.
