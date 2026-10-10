"""Seed demo users. Owner: Dev 6. Implemented in G2.

Planned usage:  python -m app.auth.seed_users
Passwords will come from environment variables, never from source code.
"""
import sys


def main() -> int:
    print("seed_users is not implemented until G2.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
