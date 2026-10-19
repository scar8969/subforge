"""v2scar command line interface.

Heavy imports (Flask-SQLAlchemy through app_factory/models) happen inside the
command body, so `python cli.py --help` works without the database layer.
"""

import argparse


def cmd_users(_args):
    from ._app import build_app as create_app
    from .models import GB, User

    app = create_app()
    with app.app_context():
        for u in User.query.order_by(User.id).all():
            print(
                f"#{u.id} {u.username}  uuid {u.vmess_uuid[:8]}…  {u.used_traffic() // GB}GB  "
                f"{'admin' if u.is_admin else 'user'}  {'ON' if u.enable else 'OFF'}"
            )
    return 0


def main():
    p = argparse.ArgumentParser(prog="v2scar", description="v2ray / shadowsocks subscription panel")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("users", help="list users")
    args = p.parse_args()
    if args.cmd == "users":
        return cmd_users(args)
    p.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover - manual entry point
    raise SystemExit(main())
