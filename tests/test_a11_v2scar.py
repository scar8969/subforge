"""A11 v2scar — tests. Run: pytest test_a11_v2scar.py"""
import sys, os, base64, json

import pytest

def test_vmess_subscription():
    from v2scar.panel.sub import generate_subscription
    class N:
        server = "hk01.example.com"
        port = 443
        name = "HK-01"
    class U:
        vmess_uuid = "3f2a9c1e-0000-0000-0000-000000000000"
    sub = generate_subscription(U(), [N()], "vmess")
    assert sub.startswith("vmess://")
    cfg = json.loads(base64.b64decode(sub[8:]))
    assert cfg["add"] == "hk01.example.com"
    assert cfg["id"] == U.vmess_uuid
