import json
import pyperclip
from urllib.parse import urlparse, parse_qs

def parse_vless(uri):
    parsed = urlparse(uri)
    userinfo = parsed.netloc.split('@')
    uuid = userinfo[0]
    server_port = userinfo[1].split(':')
    server = server_port[0]
    port = int(server_port[1])
    params = parse_qs(parsed.query)
    
    stream_settings = {
        "network": params.get("type", ["tcp"])[0],
        "security": params.get("security", ["none"])[0],
    }
    
    if stream_settings["security"] == "reality":
        stream_settings["realitySettings"] = {
            "serverName": params.get("sni", [""])[0],
            "publicKey": params.get("pbk", [""])[0],
            "shortId": params.get("sid", [""])[0],
            "fingerprint": params.get("fp", ["chrome"])[0]
        }
    
    elif stream_settings["security"] == "tls":
        stream_settings["tlsSettings"] = {
            "serverName": params.get("sni", [""])[0],
            "fingerprint": params.get("fp", ["chrome"])[0],
            "alpn": params.get("alpn", ["h2"])[0].split(',')
        }
    
    if stream_settings["network"] == "xhttp":
        stream_settings["xhttpSettings"] = {
            "host": params.get("host", [""])[0],
            "path": params.get("path", ["/"])[0],
            "mode": params.get("mode", ["packet-up"])[0]
        }
    
    elif stream_settings["network"] == "grpc":
        stream_settings["grpcSettings"] = {}
    
    elif stream_settings["network"] == "ws":
        stream_settings["wsSettings"] = {
            "path": params.get("path", [""])[0]
        }
    
    config = {
        "protocol": "vless",
        "settings": {
            "vnext": [
                {
                    "address": server,
                    "port": port,
                    "users": [
                        {
                            "id": uuid,
                            "encryption": params.get("encryption", ["none"])[0],
                            "flow": ""
                        }
                    ]
                }
            ]
        },
        "streamSettings": stream_settings,
        "tag": "proxy"
    }
    return config

def parse_ss(uri):
    parsed = urlparse(uri)
    userinfo = parsed.netloc.split('@')
    method_password = userinfo[0].split(':')
    method = method_password[0]
    password = method_password[1]
    server_port = userinfo[1].split(':')
    server = server_port[0]
    port = int(server_port[1])
    
    config = {
        "protocol": "shadowsocks",
        "settings": {
            "servers": [
                {
                    "address": server,
                    "port": port,
                    "method": method,
                    "password": password
                }
            ]
        },
        "tag": "proxy"
    }
    return config

def main():
    uri = input("Введите URI: ")
    if uri.startswith("vless://"):
        outbound_config = parse_vless(uri)
    elif uri.startswith("ss://"):
        outbound_config = parse_ss(uri)
    else:
        print("Неподдерживаемый протокол")
        return
    
    socks5_inbound = {
        "listen": "127.0.0.1",
        "port": 1080,
        "protocol": "socks",
        "settings": {
            "auth": "noauth",
            "udp": True
        },
        "sniffing": {
            "destOverride": ["http", "tls", "quic", "fakedns"],
            "enabled": False,
            "routeOnly": True
        },
        "tag": "socks"
    }
    
    freedom_outbound = {
        "protocol": "freedom",
        "tag": "direct"
    }
    
    blackhole_outbound = {
        "protocol": "blackhole",
        "tag": "block"
    }
    
    full_config = {
        "inbounds": [socks5_inbound],
        "outbounds": [outbound_config, freedom_outbound, blackhole_outbound]
    }
    
    json_config = json.dumps(full_config, indent=2)
    pyperclip.copy(json_config)
    print("Конфигурация скопирована в буфер обмена:\n", json_config)

if __name__ == "__main__":
    main()
