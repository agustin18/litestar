import pytest

from litestar import Litestar, post
from litestar.enums import RequestEncodingType
from litestar.exceptions import LitestarDeprecationWarning
from litestar.params import Body, BodyKwarg


def test_deprecated_default_warns() -> None:
    @post("/")
    async def handler(data: dict = Body()) -> None:
        pass

    with pytest.raises(LitestarDeprecationWarning, match=r"Deprecated use of 'Body\(\)' as a default value"):
        Litestar([handler])


@pytest.mark.parametrize(
    ("body_kwarg", "expected_suggestion"),
    [
        (Body(media_type="application/vnd.api+json"), "Annotated[<type>, Body(...)]"),
        (Body(media_type="application/xml"), "Annotated[<type>, Body(...)]"),
        (Body(media_type=RequestEncodingType.JSON), "JSONBody[<type>]"),
        (Body(media_type=RequestEncodingType.MESSAGEPACK), "MsgPackBody[<type>]"),
        (Body(media_type=RequestEncodingType.MULTI_PART), "MultipartBody[<type>]"),
        (Body(media_type=RequestEncodingType.URL_ENCODED), "URLEncodedBody[<type>]"),
        (Body(media_type=RequestEncodingType.JSON, min_items=1), "Annotated[<type>, Body(...)]"),
        (Body(media_type=RequestEncodingType.MULTI_PART, multipart_form_part_limit=5), "Annotated[<type>, Body(...)]"),
    ],
)
def test_deprecated_default_media_types_and_constraints(body_kwarg: BodyKwarg, expected_suggestion: str) -> None:
    @post("/")
    async def handler(data: dict = body_kwarg) -> None:  # type: ignore[assignment]
        pass

    with pytest.warns(LitestarDeprecationWarning) as record:
        Litestar([handler])

    assert len(record) == 1
    assert expected_suggestion in str(record[0].message)
