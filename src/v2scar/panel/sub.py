import base64
import json


def generate_subscription(user, nodes, sub_type="vmess"):
    lines = []
    for n in nodes:
        cfg = {
            "v": "2",
            "ps": n.name,
            "add": n.server,
            "port": n.port,
            "id": user.vmess_uuid,
            "aid": 0,
            "net": "tcp",
            "type": "none",
            "host": "",
            "path": "",
            "tls": "",
        }
        b64 = base64.b64encode(json.dumps(cfg).encode()).decode()
        lines.append(f"vmess://{b64}")
    return "\n".join(lines)
