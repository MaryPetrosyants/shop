
from drf_yasg import openapi

error_schema_400 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "error_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="ValidationError",
        ),
        "message": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additional_properties=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
            ),
            description="Keys are fields, values ​​are error messages.",
            example={"price": ["A valid number is required."]},
        ),
    },
    required=["error_type", "message"],
)
error_schema_403 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "error_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="PermissionDenied",
        ),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="You do not have permission to perform this action.",
        ),
    },
    required=["error_type", "message"],
)

error_schema_404 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "error_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="Http404",
        ),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="No Product matches the given query.",
        ),
    },
    required=["error_type", "message"],
)

error_schema_500 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "error_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="InternalServerError",
        ),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="An unexpected error occurred.",
        ),
    },
    required=["error_type", "message"],
)

