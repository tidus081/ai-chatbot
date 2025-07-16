from typing import Optional


class ChaiModelResponse:
    def __init__(
        self,
        status_code: int,
        model_output: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        self.status_code = status_code
        self.model_output = model_output
        self.model_name = model_name

    def __repr__(self):
        return (
            f"<ChaiModelResponse "
            f"status_code={self.status_code} "
            f"model_output={self.model_output!r} "
            f"model_name={self.model_name!r}>"
        )
