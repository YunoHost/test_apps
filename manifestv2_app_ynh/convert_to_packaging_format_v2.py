import copy
import json


def _convert_v1_manifest_to_v2(manifest):

    manifest = copy.deepcopy(manifest)

    if "upstream" not in manifest:
        manifest["upstream"] = {}

    if "license" in manifest and "license" not in manifest["upstream"]:
        manifest["upstream"]["license"] = manifest["license"]

    if "url" in manifest and "website" not in manifest["upstream"]:
        manifest["upstream"]["website"] = manifest["url"]

    manifest["integration"] = {
        "yunohost": manifest.get("requirements", {}).get("yunohost"),
        "architectures": "all",
        "multi_instance": manifest.get("multi_instance", False),
        "ldap": "?",
        "sso": "?",
    }

    maintainer = manifest.get("maintainer", {}).get("name")
    manifest["maintainers"] = [maintainer] if maintainer else []

    install_questions = manifest["arguments"]["install"]
    manifest["install"] = {}
    for question in install_questions:
        name = question.pop("name")
        if "ask" in question and name in ["domain", "path", "admin", "is_public", "password"]:
            question.pop("ask")
        if question.get("example") and question.get("type") in ["domain", "path", "user", "boolean", "password"]:
            question.pop("example")

        manifest["install"][name] = question

    manifest["resources"] = {
        "disk": {
            "build": "50M",     # This is an *estimate* minimum value for the disk needed at build time (e.g. during install/upgrade) and during regular usage
            "usage": "50M"      # Please only use round values such as: 10M, 100M, 200M, 400M, 800M, 1G, 2G, 4G, 8G
        },
        "ram": {
            "build": "50M",     # This is an *estimate* minimum value for the RAM needed at build time (i.e. during install/upgrade) and during regular usage
            "usage": "10M",     # Please only use round values like ["10M", "100M", "200M", "400M", "800M", "1G", "2G", "4G", "8G"]
            "include_swap": False
        },
        "route": {},
        "install_dir": {
            "base_dir": "/var/www/",  # This means that the app shall be installed in /var/www/$app which is the standard for webapps. You may change this to /opt/ if the app is a system app.
            "alias": "final_path"
        }
    }

    if "domain" in manifest["install"] and "path" in manifest["install"]:
        manifest["resources"]["route"]["url"] = "{domain}{path}"
    elif "path" not in manifest["install"]:
        manifest["resources"]["route"]["url"] = "{domain}/"
    else:
        del manifest["resources"]["route"]

    keys_to_keep = ["packaging_format", "id", "name", "description", "version", "maintainers", "upstream", "integration", "install", "resources"]

    keys_to_del = [key for key in manifest.keys() if key not in keys_to_keep]
    for key in keys_to_del:
        del manifest[key]

    return manifest


def _dump_v2_manifest_as_toml(manifest):

    import re
    from tomlkit import document, nl, table, dumps, comment

    toml_manifest = document()
    toml_manifest.add("packaging_format", 2)
    toml_manifest.add(nl())
    toml_manifest.add("id", manifest["id"])
    toml_manifest.add("name", manifest["name"])
    for lang, value in manifest["description"].items():
        toml_manifest.add(f"description.{lang}", value)
    toml_manifest.add(nl())
    toml_manifest.add("version", manifest["version"])
    toml_manifest.add(nl())
    toml_manifest.add("maintainers", manifest["maintainers"])

    upstream = table()
    for key, value in manifest["upstream"].items():
        upstream[key] = value
    toml_manifest["upstream"] = upstream

    integration = table()
    for key, value in manifest["integration"].items():
        integration[key] = value
    integration["architectures"].comment('Can be replaced by a list of supported archs using the dpkg --print-architecture nomenclature, for example: ["amd64", "i386"]')
    toml_manifest["integration"] = integration

    install = table()
    for key, value in manifest["install"].items():
        install[key] = table()
        install[key].indent(4)

        if key in ["domain", "path", "admin", "is_public", "password"]:
            install[key].add(comment("this is a generic question - ask strings are automatically handled by Yunohost's core"))

        for lang, value2 in value.get("ask", {}).items():
            install[key].add(f"ask.{lang}", value2)

        for lang, value2 in value.get("help", {}).items():
            install[key].add(f"help.{lang}", value2)

        for key2, value2 in value.items():
            if key2 in ["ask", "help"]:
                continue
            install[key].add(key2, value2)

    toml_manifest["install"] = install

    resources = table()
    for key, value in manifest["resources"].items():
        resources[key] = table()
        resources[key].indent(4)
        for key2, value2 in value.items():
            resources[key].add(key2, value2)
            if key in ["disk", "ram"] and key2 == "build":
                resources[key][key2].comment(f"This is an *estimate* minimum value for the {key} needed at build time (e.g. during install/upgrade) and during regular usage")
            elif key in ["disk", "ram"] and key2 == "usage":
                resources[key][key2].comment("Please only use round values such as: 10M, 100M, 200M, 400M, 800M, 1G, 2G, 4G, 8G")
            elif key == "install_dir" and key2 == "base_dir":
                resources[key][key2].comment("This means that the app shall be installed in /var/www/$app which is the standard for webapps. You may change this to /opt/ if the app is a system app.")

    toml_manifest["resources"] = resources

    toml_manifest_dump = dumps(toml_manifest)

    regex = re.compile(r'\"((description|ask|help)\.[a-z]{2})\"')
    toml_manifest_dump = regex.sub(r'\1', toml_manifest_dump)
    return toml_manifest_dump


manifest = json.load(open("manifest.json"))
manifest = _convert_v1_manifest_to_v2(manifest)
print(_dump_v2_manifest_as_toml(manifest))
