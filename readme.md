# Home Assistant WebSocket wrapper

The purpose of this module is to allow to execute synchronous calls to Home Assistant WebSocket API.

It is based on [Home Assistant WebSocket API](https://developers.home-assistant.io/docs/api/websocket/).

It uses synchronouse calls and short-lived connections. Which means each call will open a new connection, execute the call and close the connection.
this is way simple and fast in development, but not very efficient in terms of performance. However, it is good enough for most of the cases especially scripting the HomeAssistant.
## Usage

You can either use it with AppDaemon or without.

With AppDaemon the token and server information will be configured automatically: 
```python
from HassWS import HassWS


class appdaemon_app(hass.Hass):
    hws: HassWS

    def initialize(self):
        self.hws = HassWS(hass_instance=self)
        self.log(self.hws.send('config/entity_registry/list'))
```

Or without AppDaemon:
```python
from HassWS import HassWS

hws = HassWS(server_url='wss://my.hass.url:8123',token='token goes here')
print(hws.send('config/entity_registry/list'))
```

