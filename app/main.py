from http import HTTPStatus
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from app.ai.config_parser import config_parser, config_save
from app.ai.ollama_client import OllamaClient
from app.dto.application_response_dto import ApplicationResponseDto
from app.dto.register_application_dto import RegisterApplicationDto
from app.dto.update_application_dto import UpdateApplicationDto
from app.service.application_service import DatabaseService
from app.util.standard_response import StandardResponse

app = FastAPI()
service: DatabaseService = DatabaseService()

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content=StandardResponse(
            data=None,
            message=str(exc),
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        ).model_dump(mode="json"),
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    )

@app.get("/", response_model=StandardResponse[dict[str, str]])
async def root():
    return StandardResponse(
        data={"message": "API is running"},
        message="Success",
        status=HTTPStatus.OK,
    )

@app.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=StandardResponse[str],
)
async def register_app(data: RegisterApplicationDto):
    api_key = service.register_application(data.app_name)
    return StandardResponse(
        data=api_key,
        message="Application registered",
        status=HTTPStatus.CREATED,
    )

@app.get("/get", response_model=StandardResponse[list[ApplicationResponseDto]])
async def get_all_apps():
    return StandardResponse(
        data=service.get_applications(),
        message="Applications retrieved",
        status=HTTPStatus.OK,
    )

@app.get("/get/{id}", response_model=StandardResponse[ApplicationResponseDto])
async def get_application_by_id(id: int):
    application = service.get_application_by_id(id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return StandardResponse(
        data=application,
        message="Application retrieved",
        status=HTTPStatus.OK,
    )

@app.put(
    "/update/{id}",
    response_model=StandardResponse[ApplicationResponseDto],
)
async def update_application(id: int, data: UpdateApplicationDto):
    application = service.update_application(id, data.app_name)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return StandardResponse(
        data=application,
        message="Application updated",
        status=HTTPStatus.OK,
    )

@app.delete(
    "/delete/{id}",
    response_model=StandardResponse[None],
)
async def delete_application(id: int):
    if not service.delete_application(id):
        raise HTTPException(status_code=404, detail="Application not found")

    return StandardResponse(
        data=None,
        message="Application deleted",
        status=HTTPStatus.OK,
    )

@app.get(
    "/ai",
    response_model=StandardResponse[str]
)
async def get_response(file_path: str, prompt: str):
    print(file_path)
    config = config_parser(file_path=file_path)
    if (config["provider"] == "ollama"):
        ai = OllamaClient(config["role"], config["instructions"], config["history"], config["model"])
        response = await ai.generate_response(
            {
                "prompt": prompt
            }
        )

        config_save(file_path=file_path, message=prompt, role="user")
        config_save(file_path=file_path, message=response, role="ai")
        

        return StandardResponse(
            data=response,
            message="Successfully queried ai",
            status=HTTPStatus.OK
        )
