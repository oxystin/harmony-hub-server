from aioharmony.harmonyapi import HarmonyAPI, SendCommandDevice
from aiohttp import web
import jinja2
import aiohttp_jinja2
import json
import os

HUB_IP = os.environ.get("HUB_IP")
HUB_PROTOCOL = os.environ.get("HUB_PROTOCOL") or "WEBSOCKETS"
WEB_PORT = os.environ.get("WEB_PORT") or 32670


async def get_client():
    client = HarmonyAPI(HUB_IP, HUB_PROTOCOL)
    try:
        if await client.connect():
            return client
    except:
        pass
    return None


async def connect_hub(request):
    client = await get_client()
    if client is not None:
        config = client.json_config
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
    if request.body_exists:
        json_data = await request.json()
        device = json_data.get("id")
        command = json_data.get("command")
        client = await get_client()
        if client is not None:
            send_command_args = SendCommandDevice(
                device=device,
                command=command,
                delay=0,
            )
            res = await client.send_commands(send_command_args)
            await client.close()
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
    else:
        return web.json_response(
            {
                "status": "Bad Request",
                "message": "It is necessary to transfer the device id and command name in JSON format. Example: {'id': '38213988', 'command': 'Stereo'}",
            },
            status=400,
        )


app = web.Application()

# setup jinja2
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), "templates")
    ),
)
app["static_root_url"] = "/static"
app.router.add_static("/static", "./static")
app.router.add_get("/", connect_hub)
app.router.add_post("/command", send_command)

if __name__ == "__main__":
    web.run_app(app, port=int(WEB_PORT))
