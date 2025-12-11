from fastapi import Request


def parse_model_factory(model_class):
    async def _dep(request: Request):
        ct = request.headers.get("content-type", "")
        if "application/json" in ct:
            data = await request.json()
        else:
            form = await request.form()
            data = {k: v for k, v in form.items()}
        return model_class(**data)

    return _dep
