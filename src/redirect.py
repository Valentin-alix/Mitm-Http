import asyncio
import json
import threading
from dataclasses import dataclass

from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster


@dataclass
class ChangeDofusConfig:
    dump_master: DumpMaster

    async def response(self, flow: http.HTTPFlow):
        if (
            (
                flow.request.pretty_url
                == "https://dofus2.cdn.ankama.com/config/beta_windows.json"
            )
            and flow.response
            and flow.response.content
        ):
            datas = json.loads(flow.response.content)
            datas["connectionHosts"] = ["Beta:localhost:5555"]
            flow.response.content = json.dumps(datas).encode("utf-8")


async def start_proxy_dofus_config(with_logs: bool = False):
    opts = options.Options(listen_host="127.0.0.1", listen_port=8080)
    dump_master = DumpMaster(opts, with_termlog=with_logs, with_dumper=with_logs)

    addon = ChangeDofusConfig(dump_master)
    dump_master.addons.add(addon)

    try:
        await dump_master.run()
    except KeyboardInterrupt:
        dump_master.shutdown()


def run_proxy_config_in_thread(with_logs: bool = False):
    thread = threading.Thread(
        target=lambda: asyncio.run(start_proxy_dofus_config(with_logs)), daemon=True
    )
    thread.start()
    return thread


# Dont forget to add proxy to redirect to localhost 8080

if __name__ == "__main__":
    thread = run_proxy_config_in_thread(True)
    thread.join()
