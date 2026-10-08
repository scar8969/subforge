== curl ==
# GET  /api/subscribe?token=1&sub_type=vmess
# POST /api/traffic -H "X-API-Token: dev-api-token"  {"node_id":1,"users":[{"id":1,"upload":1024,"download":2048}]}
# POST /api/admin/users  {"username":"bob","traffic":10737418240}
# GET  /api/admin/analytics
# CLI: v2scar users

== session plan ==
# Session 1: models + seed + subscribe (vmess://) + traffic sync → tests
# Session 2: admin CRUD + analytics → tests
# Session 3: web templates + cli → screenshots → README → CI/Docker/Pages → tag
