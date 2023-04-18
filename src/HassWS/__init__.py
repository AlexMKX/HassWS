from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import appdaemon.plugins.hass.hassapi as hass

from typing import Optional
import websocket

import json
import urllib.parse


class HassWS:
    _hass: 'hass.Hass'
    _url: str
    _token: str

    class Error(Exception):
        pass

    def __init__(self, hass_instance: Optional['hass.Hass'] = None,
                 server_url: Optional[str] = None, token: Optional[str] = None):
        if hass_instance is not None:
            ha_url = hass_instance.config['plugins']['HASS']['ha_url']
            ha_srv = urllib.parse.urlparse(ha_url).netloc
            self._url = f"wss://{ha_srv}/api/websocket"
            self._token = hass_instance.config['plugins']['HASS']['token']
        else:
            if not (server_url is not None and token is not None):
                raise self.Error('Either hass_instance or server_url and token must be provided')
            ha_srv = urllib.parse.urlparse(server_url).netloc
            self._url = f"wss://{ha_srv}/api/websocket"
            self._token = token

    def __connect(self) -> websocket.WebSocket:
        ws = websocket.create_connection(self._url)
        msg = json.loads(ws.recv())
        if msg['type'] != 'auth_required':
            raise self.Error('Unexpected message type: {}'.format(msg['type']))
        ws.send(json.dumps({"type": "auth", "access_token": self._token}))
        msg = json.loads(ws.recv())
        if msg['type'] != 'auth_ok':
            raise self.Error('Unexpected message type: {}'.format(msg['type']))
        return ws

    def send(self, msg: str, **kwargs):
        ws = self.__connect()
        msg_data = kwargs
        msg_data['type'] = msg
        msg_data['id'] = 1
        ws.send(json.dumps(msg_data))
        resp_j = ws.recv()
        resp = json.loads(resp_j)
        if not (resp['type'] == 'result' and resp['success'] and resp['id'] == 1):
            raise self.Error('Unexpected message type: {}'.format(resp))
        return resp['result']
