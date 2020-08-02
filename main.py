from aioharmony.harmonyapi import HarmonyAPI, SendCommandDevice
from aiohttp import web
import jinja2
import aiohttp_jinja2
import json
import os

HUB_IP = os.environ.get("HUB_IP")
HUB_PROTOCOL = os.environ.get("HUB_PROTOCOL") or "WEBSOCKETS"


async def get_client():
    client = HarmonyAPI(HUB_IP, HUB_PROTOCOL)
    try:
        if await client.connect():
            return client
    except:
        pass
    return None


async def show_config(client):
    config = client.config
    if config:
        return client.json_config
    else:
        return None


async def connect_hub(request):
    client = await get_client()
    if client is not None:
        config = await show_config(client)
        hub_info = {
            "Hub_Info": {
                "name": client.name,
                "ip": client.ip_address,
                "fw": client.fw_version,
                "id": client.hub_id,
                "protocol": client.protocol,
            }
        }
        await client.close()
        response = aiohttp_jinja2.render_template(
            "index.html", request, {**hub_info, **config}
        )
        return response
    else:
        return web.json_response(
            {"status": "ERROR", "message": "HUB not connect"}, status=404
        )


async def send_command(request):
    client = await get_client()
    if client is not None:
        send_command_args = SendCommandDevice(
            device=request.match_info["id_device"],
            command=request.match_info["command"],
            delay=0,
        )
        res = await client.send_commands(send_command_args)
        if res:
            return web.json_response(
                {"status": "Bad Request", "message": res[0].msg}, status=400
            )
        else:
            return web.json_response(
                {"status": "ok", "message": "Command sent successfully"}
            )
    else:
        return web.json_response(
            {"status": "ERROR", "message": "HUB not connect"}, status=404
        )


app = web.Application()

# setup jinja2
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), "templates")
    ),
)

app.router.add_get("/", connect_hub)
app.router.add_get("/device/command/{id_device}/{command}", send_command)

if __name__ == "__main__":
    web.run_app(app, port=32670)
