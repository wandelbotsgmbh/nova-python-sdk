import json

import wandelbots_api_client as wb


class ControllerNotFoundException(Exception):
    def __init__(self, controller: str = None):
        super().__init__(f"Controller {controller} not found.")


class PlanTrajectoryFailed(Exception):
    def __init__(self, error: wb.models.PlanTrajectoryFailedResponse):
        super().__init__(f"Plan trajectory failed: {json.dumps(error.to_dict(), indent=2)}")