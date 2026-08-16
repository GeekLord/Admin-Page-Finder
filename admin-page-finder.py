#!/usr/bin/env python3
# Admin Page Finder Script (Legacy - Standalone)
# Modernized to Python 3 with http.client
# For the full-featured async scanner, use: pip install -e . && apf scan <url>

import http.client
import socket
import sys


try:
    var1 = 0
    var2 = 0

    php = [
        "admin/", "administrator/", "admin1/", "admin2/", "admin3/", "admin4/",
        "admin5/", "usuarios/", "usuario/", "moderator/", "webadmin/", "adminarea/",
        "bb-admin/", "adminLogin/", "admin_area/", "panel-administracion/", "instadmin/",
        "memberadmin/", "administratorlogin/", "adm/",
        "admin/account.php", "admin/index.php", "admin/login.php", "admin/admin.php",
        "admin_area/admin.php", "admin_area/login.php", "siteadmin/login.php",
        "siteadmin/index.php", "siteadmin/login.html",
        "admin/account.html", "admin/index.html", "admin/login.html", "admin/admin.html",
        "admin_area/index.php", "bb-admin/index.php", "bb-admin/login.php", "bb-admin/admin.php",
        "admin/home.php", "admin_area/login.html", "admin_area/index.html",
        "admin/controlpanel.php", "admin.php", "admincp/index.asp", "admincp/login.asp",
        "admincp/index.html", "adminpanel.html", "webadmin.html",
        "webadmin/index.html", "webadmin/admin.html", "webadmin/login.html",
        "admin/admin_login.html", "admin_login.html", "panel-administracion/login.html",
        "admin/cp.php", "cp.php", "administrator/index.php", "administrator/login.php",
        "nsw/admin/login.php", "webadmin/login.php", "admin/admin_login.php", "admin_login.php",
        "administrator/account.php", "administrator.php", "admin_area/admin.html",
        "pages/admin/admin-login.php", "admin/admin-login.php", "admin-login.php",
        "bb-admin/index.html", "bb-admin/login.html", "bb-admin/admin.html",
        "admin/home.html", "login.php", "modelsearch/login.php", "moderator.php",
        "moderator/login.php", "moderator/admin.php", "account.php",
        "pages/admin/admin-login.html", "admin/admin-login.html", "admin-login.html",
        "controlpanel.php", "admincontrol.php", "admin/adminLogin.html", "adminLogin.html",
        "home.html", "rcjakar/admin/login.php", "adminarea/index.html", "adminarea/admin.html",
        "webadmin.php", "webadmin/index.php", "webadmin/admin.php",
        "admin/controlpanel.html", "admin.html", "admin/cp.html", "cp.html",
        "adminpanel.php", "moderator.html", "administrator/index.html",
        "administrator/login.html", "user.html", "administrator/account.html",
        "administrator.html", "login.html", "modelsearch/login.html",
        "moderator/login.html", "adminarea/login.html",
        "panel-administracion/index.html", "panel-administracion/admin.html",
        "modelsearch/index.html", "modelsearch/admin.html",
        "admincontrol/login.html", "adm/index.html", "adm.html", "moderator/admin.html",
        "user.php", "account.html", "controlpanel.html", "admincontrol.html",
        "panel-administracion/login.php", "wp-login.php", "adminLogin.php",
        "admin/adminLogin.php", "home.php", "adminarea/index.php",
        "adminarea/admin.php", "adminarea/login.php",
        "panel-administracion/index.php", "panel-administracion/admin.php",
        "modelsearch/index.php", "modelsearch/admin.php", "admincontrol/login.php",
        "adm/admloginuser.php", "admloginuser.php", "admin2.php",
        "admin2/login.php", "admin2/index.php", "usuarios/login.php",
        "adm/index.php", "adm.php", "affiliate.php", "adm_auth.php",
        "memberadmin.php", "administratorlogin.php",
        # Modern PHP frameworks
        "wp-admin/", "wp-admin/admin-ajax.php", "wp-admin/setup-config.php",
        "wp-json/wp/v2/users", "xmlrpc.php",
        "nova/", "nova/login", "telescope/", "horizon/", "horizon/dashboard",
        "pulse/", "filament/", "filament/admin", "filament/login",
        "backend/backend/auth/signin",
        "typo3/", "typo3/login", "typo3/index.php",
        "phpmyadmin/", "phpmyadmin/index.php", "pma/", "myadmin/",
        "adminer/", "adminer.php",
    ]

    asp = [
        "admin/", "administrator/", "admin1/", "admin2/", "admin3/", "admin4/",
        "admin5/", "moderator/", "webadmin/", "adminarea/", "bb-admin/", "adminLogin/",
        "admin_area/", "panel-administracion/", "instadmin/",
        "memberadmin/", "administratorlogin/", "adm/",
        "account.asp", "admin/account.asp", "admin/index.asp", "admin/login.asp",
        "admin/admin.asp", "admin_area/admin.asp", "admin_area/login.asp",
        "admin/account.html", "admin/index.html", "admin/login.html", "admin/admin.html",
        "admin_area/admin.html", "admin_area/login.html", "admin_area/index.html",
        "admin_area/index.asp", "bb-admin/index.asp", "bb-admin/login.asp",
        "bb-admin/admin.asp", "bb-admin/index.html", "bb-admin/login.html",
        "bb-admin/admin.html", "admin/home.html", "admin/controlpanel.html",
        "admin.html", "admin/cp.html", "cp.html",
        "administrator/index.html", "administrator/login.html",
        "administrator/account.html", "administrator.html",
        "login.html", "modelsearch/login.html", "moderator.html",
        "moderator/login.html", "moderator/admin.html",
        "account.html", "controlpanel.html", "admincontrol.html",
        "admin_login.html", "panel-administracion/login.html",
        "admin/home.asp", "admin/controlpanel.asp", "admin.asp",
        "pages/admin/admin-login.asp", "admin/admin-login.asp", "admin-login.asp",
        "admin/cp.asp", "cp.asp", "administrator/account.asp", "administrator.asp",
        "acceso.asp", "login.asp", "modelsearch/login.asp",
        "moderator.asp", "moderator/login.asp", "administrator/login.asp",
        "moderator/admin.asp", "controlpanel.asp", "adminpanel.html",
        "webadmin.html", "pages/admin/admin-login.html", "admin/admin-login.html",
        "webadmin/index.html", "webadmin/admin.html", "webadmin/login.html",
        "user.asp", "user.html", "admincp/index.asp", "admincp/login.asp",
        "admincp/index.html", "admin/adminLogin.html", "adminLogin.html",
        "home.html", "adminarea/index.html", "adminarea/admin.html",
        "adminarea/login.html", "panel-administracion/index.html",
        "panel-administracion/admin.html", "modelsearch/index.html",
        "modelsearch/admin.html", "admin/admin_login.html",
        "admincontrol/login.html", "adm/index.html", "adm.html",
        "admincontrol.asp", "admin/account.asp", "adminpanel.asp",
        "webadmin.asp", "webadmin/index.asp", "webadmin/admin.asp",
        "webadmin/login.asp", "admin/admin_login.asp", "admin_login.asp",
        "panel-administracion/login.asp", "adminLogin.asp",
        "admin/adminLogin.asp", "home.asp", "adminarea/index.asp",
        "adminarea/admin.asp", "adminarea/login.asp", "admin-login.html",
        "panel-administracion/index.asp", "panel-administracion/admin.asp",
        "modelsearch/index.asp", "modelsearch/admin.asp",
        "administrator/index.asp", "admincontrol/login.asp",
        "adm/admloginuser.asp", "admloginuser.asp", "admin2.asp",
        "admin2/login.asp", "admin2/index.asp", "adm/index.asp",
        "adm.asp", "affiliate.asp", "adm_auth.asp",
        "memberadmin.asp", "administratorlogin.asp",
        "siteadmin/login.asp", "siteadmin/index.asp", "siteadmin/login.html",
    ]

    cfm = [
        "admin/", "administrator/", "admin1/", "admin2/", "admin3/", "admin4/",
        "admin5/", "usuarios/", "usuario/", "moderator/", "webadmin/", "adminarea/",
        "bb-admin/", "adminLogin/", "admin_area/", "panel-administracion/", "instadmin/",
        "memberadmin/", "administratorlogin/", "adm/",
        "admin/account.cfm", "admin/index.cfm", "admin/login.cfm", "admin/admin.cfm",
        "admin_area/admin.cfm", "admin_area/login.cfm",
        "siteadmin/login.cfm", "siteadmin/index.cfm", "siteadmin/login.html",
        "admin/account.html", "admin/index.html", "admin/login.html", "admin/admin.html",
        "admin_area/index.cfm", "bb-admin/index.cfm", "bb-admin/login.cfm",
        "bb-admin/admin.cfm", "admin/home.cfm", "admin_area/login.html",
        "admin_area/index.html", "admin/controlpanel.cfm", "admin.cfm",
        "admincp/index.asp", "admincp/login.asp", "admincp/index.html",
        "adminpanel.html", "webadmin.html", "webadmin/index.html",
        "webadmin/admin.html", "webadmin/login.html",
        "admin/admin_login.html", "admin_login.html", "panel-administracion/login.html",
        "admin/cp.cfm", "cp.cfm", "administrator/index.cfm", "administrator/login.cfm",
        "nsw/admin/login.cfm", "webadmin/login.cfm",
        "admin/admin_login.cfm", "admin_login.cfm",
        "administrator/account.cfm", "administrator.cfm", "admin_area/admin.html",
        "pages/admin/admin-login.cfm", "admin/admin-login.cfm", "admin-login.cfm",
        "bb-admin/index.html", "bb-admin/login.html", "bb-admin/admin.html",
        "admin/home.html", "login.cfm", "modelsearch/login.cfm",
        "moderator.cfm", "moderator/login.cfm", "moderator/admin.cfm",
        "account.cfm", "pages/admin/admin-login.html", "admin/admin-login.html",
        "admin-login.html", "controlpanel.cfm", "admincontrol.cfm",
        "admin/adminLogin.html", "acceso.cfm", "adminLogin.html",
        "home.html", "rcjakar/admin/login.cfm", "adminarea/index.html",
        "adminarea/admin.html", "webadmin.cfm", "webadmin/index.cfm",
        "webadmin/admin.cfm", "admin/controlpanel.html", "admin.html",
        "admin/cp.html", "cp.html", "adminpanel.cfm", "moderator.html",
        "administrator/index.html", "administrator/login.html", "user.html",
        "administrator/account.html", "administrator.html", "login.html",
        "modelsearch/login.html", "moderator/login.html", "adminarea/login.html",
        "panel-administracion/index.html", "panel-administracion/admin.html",
        "modelsearch/index.html", "modelsearch/admin.html",
        "admincontrol/login.html", "adm/index.html", "adm.html",
        "moderator/admin.html", "user.cfm", "account.html",
        "controlpanel.html", "admincontrol.html",
        "panel-administracion/login.cfm", "wp-login.cfm",
        "adminLogin.cfm", "admin/adminLogin.cfm", "home.cfm",
        "adminarea/index.cfm", "adminarea/admin.cfm", "adminarea/login.cfm",
        "panel-administracion/index.cfm", "panel-administracion/admin.cfm",
        "modelsearch/index.cfm", "modelsearch/admin.cfm",
        "admincontrol/login.cfm", "adm/admloginuser.cfm", "admloginuser.cfm",
        "admin2.cfm", "admin2/login.cfm", "admin2/index.cfm",
        "usuarios/login.cfm", "adm/index.cfm", "adm.cfm",
        "affiliate.cfm", "adm_auth.cfm", "memberadmin.cfm", "administratorlogin.cfm",
    ]

    js = [
        "admin/", "administrator/", "admin1/", "admin2/", "admin3/", "admin4/",
        "admin5/", "usuarios/", "usuario/", "moderator/", "webadmin/", "adminarea/",
        "bb-admin/", "adminLogin/", "admin_area/", "panel-administracion/", "instadmin/",
        "memberadmin/", "administratorlogin/", "adm/",
        "admin/account.js", "admin/index.js", "admin/login.js", "admin/admin.js",
        "admin_area/admin.js", "admin_area/login.js",
        "siteadmin/login.js", "siteadmin/index.js", "siteadmin/login.html",
        "admin/account.html", "admin/index.html", "admin/login.html", "admin/admin.html",
        "admin_area/index.js", "bb-admin/index.js", "bb-admin/login.js",
        "bb-admin/admin.js", "admin/home.js", "admin_area/login.html",
        "admin_area/index.html", "admin/controlpanel.js", "admin.js",
        "admincp/index.asp", "admincp/login.asp", "admincp/index.html",
        "adminpanel.html", "webadmin.html", "webadmin/index.html",
        "webadmin/admin.html", "webadmin/login.html",
        "admin/admin_login.html", "admin_login.html", "panel-administracion/login.html",
        "admin/cp.js", "cp.js", "administrator/index.js", "administrator/login.js",
        "nsw/admin/login.js", "webadmin/login.js",
        "admin/admin_login.js", "admin_login.js",
        "administrator/account.js", "administrator.js", "admin_area/admin.html",
        "pages/admin/admin-login.js", "admin/admin-login.js", "admin-login.js",
        "bb-admin/index.html", "bb-admin/login.html", "bb-admin/admin.html",
        "admin/home.html", "login.js", "modelsearch/login.js",
        "moderator.js", "moderator/login.js", "moderator/admin.js",
        "account.js", "pages/admin/admin-login.html", "admin/admin-login.html",
        "admin-login.html", "controlpanel.js", "admincontrol.js",
        "admin/adminLogin.html", "adminLogin.html",
        "home.html", "rcjakar/admin/login.js", "adminarea/index.html",
        "adminarea/admin.html", "webadmin.js", "webadmin/index.js", "acceso.js",
        "webadmin/admin.js", "admin/controlpanel.html", "admin.html",
        "admin/cp.html", "cp.html", "adminpanel.js", "moderator.html",
        "administrator/index.html", "administrator/login.html", "user.html",
        "administrator/account.html", "administrator.html", "login.html",
        "modelsearch/login.html", "moderator/login.html", "adminarea/login.html",
        "panel-administracion/index.html", "panel-administracion/admin.html",
        "modelsearch/index.html", "modelsearch/admin.html",
        "admincontrol/login.html", "adm/index.html", "adm.html",
        "moderator/admin.html", "user.js", "account.html",
        "controlpanel.html", "admincontrol.html",
        "panel-administracion/login.js", "wp-login.js",
        "adminLogin.js", "admin/adminLogin.js", "home.js",
        "adminarea/index.js", "adminarea/admin.js", "adminarea/login.js",
        "panel-administracion/index.js", "panel-administracion/admin.js",
        "modelsearch/index.js", "modelsearch/admin.js",
        "admincontrol/login.js", "adm/admloginuser.js", "admloginuser.js",
        "admin2.js", "admin2/login.js", "admin2/index.js",
        "usuarios/login.js", "adm/index.js", "adm.js",
        "affiliate.js", "adm_auth.js", "memberadmin.js", "administratorlogin.js",
        # Modern JS framework admin paths
        "keystone/signin", "strapi/admin", "strapi/admin/auth/login",
        "directus/", "directus/admin", "ghost/ghost/", "ghost/admin/",
        "payload/admin", "studio/", "studio/desk", "sanity/desk",
        "tina/", "tina/admin", "admin/index.html", "decap/",
        "nextadmin/", "medusa/", "admin-ui/",
        "api/admin", "api/auth/signin", "api/auth/session",
    ]

    cgi = [
        "admin/", "administrator/", "admin1/", "admin2/", "admin3/", "admin4/",
        "admin5/", "usuarios/", "usuario/", "moderator/", "webadmin/", "adminarea/",
        "bb-admin/", "adminLogin/", "admin_area/", "panel-administracion/", "instadmin/",
        "memberadmin/", "administratorlogin/", "adm/",
        "admin/account.cgi", "admin/index.cgi", "admin/login.cgi", "admin/admin.cgi",
        "admin_area/admin.cgi", "admin_area/login.cgi",
        "siteadmin/login.cgi", "siteadmin/index.cgi", "siteadmin/login.html",
        "admin/account.html", "admin/index.html", "admin/login.html", "admin/admin.html",
        "admin_area/index.cgi", "bb-admin/index.cgi", "bb-admin/login.cgi",
        "bb-admin/admin.cgi", "admin/home.cgi", "admin_area/login.html",
        "admin_area/index.html", "admin/controlpanel.cgi", "admin.cgi",
        "admincp/index.asp", "admincp/login.asp", "admincp/index.html",
        "adminpanel.html", "webadmin.html", "webadmin/index.html",
        "webadmin/admin.html", "webadmin/login.html",
        "admin/admin_login.html", "admin_login.html", "panel-administracion/login.html",
        "admin/cp.cgi", "cp.cgi", "administrator/index.cgi", "administrator/login.cgi",
        "nsw/admin/login.cgi", "webadmin/login.cgi",
        "admin/admin_login.cgi", "admin_login.cgi",
        "administrator/account.cgi", "administrator.cgi", "admin_area/admin.html",
        "pages/admin/admin-login.cgi", "admin/admin-login.cgi", "admin-login.cgi",
        "bb-admin/index.html", "bb-admin/login.html", "bb-admin/admin.html",
        "admin/home.html", "login.cgi", "modelsearch/login.cgi",
        "moderator.cgi", "moderator/login.cgi", "moderator/admin.cgi",
        "account.cgi", "pages/admin/admin-login.html", "admin/admin-login.html",
        "admin-login.html", "controlpanel.cgi", "admincontrol.cgi",
        "admin/adminLogin.html", "adminLogin.html",
        "home.html", "rcjakar/admin/login.cgi", "adminarea/index.html",
        "adminarea/admin.html", "webadmin.cgi", "webadmin/index.cgi", "acceso.cgi",
        "webadmin/admin.cgi", "admin/controlpanel.html", "admin.html",
        "admin/cp.html", "cp.html", "adminpanel.cgi", "moderator.html",
        "administrator/index.html", "administrator/login.html", "user.html",
        "administrator/account.html", "administrator.html", "login.html",
        "modelsearch/login.html", "moderator/login.html", "adminarea/login.html",
        "panel-administracion/index.html", "panel-administracion/admin.html",
        "modelsearch/index.html", "modelsearch/admin.html",
        "admincontrol/login.html", "adm/index.html", "adm.html",
        "moderator/admin.html", "user.cgi", "account.html",
        "controlpanel.html", "admincontrol.html",
        "panel-administracion/login.cgi", "wp-login.cgi",
        "adminLogin.cgi", "admin/adminLogin.cgi", "home.cgi",
        "adminarea/index.cgi", "adminarea/admin.cgi", "adminarea/login.cgi",
        "panel-administracion/index.cgi", "panel-administracion/admin.cgi",
        "modelsearch/index.cgi", "modelsearch/admin.cgi",
        "admincontrol/login.cgi", "adm/admloginuser.cgi", "admloginuser.cgi",
        "admin2.cgi", "admin2/login.cgi", "admin2/index.cgi",
        "usuarios/login.cgi", "adm/index.cgi", "adm.cgi",
        "affiliate.cgi", "adm_auth.cgi", "memberadmin.cgi", "administratorlogin.cgi",
    ]

    brf = [
        "admin/", "administrator/", "admin1/", "admin2/", "admin3/", "admin4/",
        "admin5/", "usuarios/", "usuario/", "moderator/", "webadmin/", "adminarea/",
        "bb-admin/", "adminLogin/", "admin_area/", "panel-administracion/", "instadmin/",
        "memberadmin/", "administratorlogin/", "adm/",
        "admin/account.brf", "admin/index.brf", "admin/login.brf", "admin/admin.brf",
        "admin_area/admin.brf", "admin_area/login.brf",
        "siteadmin/login.brf", "siteadmin/index.brf", "siteadmin/login.html",
        "admin/account.html", "admin/index.html", "admin/login.html", "admin/admin.html",
        "admin_area/index.brf", "bb-admin/index.brf", "bb-admin/login.brf",
        "bb-admin/admin.brf", "admin/home.brf", "admin_area/login.html",
        "admin_area/index.html", "admin/controlpanel.brf", "admin.brf",
        "admincp/index.asp", "admincp/login.asp", "admincp/index.html",
        "adminpanel.html", "webadmin.html", "webadmin/index.html",
        "webadmin/admin.html", "webadmin/login.html",
        "admin/admin_login.html", "admin_login.html", "panel-administracion/login.html",
        "admin/cp.brf", "cp.brf", "administrator/index.brf", "administrator/login.brf",
        "nsw/admin/login.brf", "webadmin/login.brf",
        "admin/admin_login.brf", "admin_login.brf",
        "administrator/account.brf", "administrator.brf", "acceso.brf",
        "admin_area/admin.html", "pages/admin/admin-login.brf",
        "admin/admin-login.brf", "admin-login.brf",
        "bb-admin/index.html", "bb-admin/login.html", "bb-admin/admin.html",
        "admin/home.html", "login.brf", "modelsearch/login.brf",
        "moderator.brf", "moderator/login.brf", "moderator/admin.brf",
        "account.brf", "pages/admin/admin-login.html", "admin/admin-login.html",
        "admin-login.html", "controlpanel.brf", "admincontrol.brf",
        "admin/adminLogin.html", "adminLogin.html",
        "home.html", "rcjakar/admin/login.brf", "adminarea/index.html",
        "adminarea/admin.html", "webadmin.brf", "webadmin/index.brf",
        "webadmin/admin.brf", "admin/controlpanel.html", "admin.html",
        "admin/cp.html", "cp.html", "adminpanel.brf", "moderator.html",
        "administrator/index.html", "administrator/login.html", "user.html",
        "administrator/account.html", "administrator.html", "login.html",
        "modelsearch/login.html", "moderator/login.html", "adminarea/login.html",
        "panel-administracion/index.html", "panel-administracion/admin.html",
        "modelsearch/index.html", "modelsearch/admin.html",
        "admincontrol/login.html", "adm/index.html", "adm.html",
        "moderator/admin.html", "user.brf", "account.html",
        "controlpanel.html", "admincontrol.html",
        "panel-administracion/login.brf", "wp-login.brf",
        "adminLogin.brf", "admin/adminLogin.brf", "home.brf",
        "adminarea/index.brf", "adminarea/admin.brf", "adminarea/login.brf",
        "panel-administracion/index.brf", "panel-administracion/admin.brf",
        "modelsearch/index.brf", "modelsearch/admin.brf",
        "admincontrol/login.brf", "adm/admloginuser.brf", "admloginuser.brf",
        "admin2.brf", "admin2/login.brf", "admin2/index.brf",
        "usuarios/login.brf", "adm/index.brf", "adm.brf",
        "affiliate.brf", "adm_auth.brf", "memberadmin.brf", "administratorlogin.brf",
    ]

    # Modern framework paths (framework-agnostic)
    modern = [
        # DevOps / Monitoring
        "grafana/", "grafana/login", "kibana/", "kibana/app/",
        "prometheus/", "prometheus/graph", "prometheus/targets",
        "jenkins/", "jenkins/login", "jenkins/manage",
        "portainer/", "traefik/", "traefik/dashboard/",
        "argocd/", "argocd/login",
        "rancher/", "rancher/login",
        "kubernetes-dashboard/",
        "consul/", "vault/", "nomad/",
        # Database admin
        "pgadmin/", "pgadmin4/", "pgadmin4/login",
        "mongo-express/", "redis-commander/",
        "cloudbeaver/", "adminer/", "phpmyadmin/",
        "minio/", "minio/login", "minio/console/",
        # Auth / Identity
        "keycloak/", "keycloak/admin/", "keycloak/auth/",
        "auth/admin/", "auth/realms/master/",
        "authentik/", "if/admin/",
        "fusionauth/", "dex/", "authelia/", "zitadel/",
        # E-commerce
        "shopware/", "saleor/", "spree/admin",
        # Misc modern
        "n8n/", "budibase/", "appsmith/", "retool/",
        "nocodb/", "metabase/", "redash/",
        "outline/", "bookstack/", "gitea/",
        "mattermost/", "rocketchat/",
        "homeassistant/", "proxmox/",
        "webmin/", "cockpit/", "netdata/",
    ]

    try:
        site = input("Write Target WebSite For Scan: ")
        site = site.replace("http://", "").replace("https://", "")
        site = site.rstrip("/")
        print(f"\tChecking website {site}...")
        conn = http.client.HTTPConnection(site, timeout=10)
        conn.request("HEAD", "/")
        conn.getresponse()
        print("\t[$] Yes... Server is Online.")
        conn.close()
    except (http.client.HTTPException, socket.error, OSError) as e:
        input(f"\t [!] Oops Error occurred, Server offline or invalid URL: {e}")
        sys.exit(1)

    print("Enter site source code:")
    print("1) PHP")
    print("2) ASP")
    print("3) CFM")
    print("4) JS")
    print("5) CGI")
    print("6) BRF")
    print("7) Modern (DevOps/DB/Auth/E-commerce)")
    print("\nPress number and Enter to select\n")
    code = input("> ").strip()

    wordlists = {
        "1": ("PHP", php),
        "2": ("ASP", asp),
        "3": ("CFM", cfm),
        "4": ("JS", js),
        "5": ("CGI", cgi),
        "6": ("BRF", brf),
        "7": ("Modern", modern),
    }

    if code not in wordlists:
        print("[!] Invalid selection. Exiting.")
        sys.exit(1)

    name, paths = wordlists[code]
    print(f"\t [+] Scanning {site} with {name} wordlist ({len(paths)} paths)...\n")

    for admin in paths:
        admin = admin.replace("\n", "")
        admin_path = "/" + admin
        host = site + admin_path
        print(f"\t [#] Checking {host}...")
        try:
            connection = http.client.HTTPConnection(site, timeout=10)
            connection.request("GET", admin_path)
            response = connection.getresponse()
            var2 += 1
            if response.status == 200:
                var1 += 1
                print(f"\n\n>>> {host} Admin page found!")
                input("Press enter to continue scanning.\n")
            elif response.status == 404:
                pass
            elif response.status in (301, 302, 303, 307, 308):
                location = response.getheader("Location", "")
                print(f"\n>>> {host} Possible admin page ({response.status} -> {location})")
            else:
                print(f"{host} Interesting response: {response.status}")
            connection.close()
        except (http.client.HTTPException, socket.error, OSError):
            pass

    print("\n\nCompleted!\n")
    print(f"{var1} Admin Page(s) Found!")
    print(f"{var2} Total Page(s) Scanned!")
    input("[/] Scan complete. Press Enter to exit.")

except (KeyboardInterrupt, SystemExit):
    print("\n\t[!] Session Cancelled!")
except Exception as e:
    print(f"\n\t[!] Session Cancelled; Error Occurred: {e}")
