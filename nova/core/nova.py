from nova.core.controller import Controller
from nova.core.exceptions import ControllerNotFoundException
from nova.gateway import ApiGateway


class Nova:
    def __init__(
        self,
        *,
        host: str | None = None,
        username: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
        version: str = "v1",
    ):
        self._api_client = ApiGateway(
            host=host,
            username=username,
            password=password,
            access_token=access_token,
            version=version,
        )

    def cell(self, cell_id: str = "cell") -> "Cell":
        return Cell(self._api_client, cell_id)


class Cell:
    def __init__(self, api_gateway: ApiGateway, cell_id: str):
        self._api_gateway = api_gateway
        self._cell_id = cell_id

    async def controller(self, controller_host: str = None) -> "Controller":
        controller_api = self._api_gateway.controller_api
        controller_list = await controller_api.list_controllers(cell=self._cell_id)
        found_controller = next(
            (c for c in controller_list.instances if c.host == controller_host), None
        )

        if found_controller is None:
            raise ControllerNotFoundException(controller=controller_host)

        return Controller(
            api_gateway=self._api_gateway, cell=self._cell_id, controller_host=found_controller.host
        )
