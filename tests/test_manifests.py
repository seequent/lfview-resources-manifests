import pytest

from lfview.resources import files, spatial, manifests
import properties


def test_types():
    assert manifests.View.BASE_TYPE == 'views'
    assert getattr(manifests.View, 'SUB_TYPE', None) is None


@pytest.mark.parametrize('name', [properties.undefined, 'My View'])
@pytest.mark.parametrize(
    'description', [properties.undefined, 'Some description']
)
@pytest.mark.parametrize('label_x', [properties.undefined, 'Label 1'])
@pytest.mark.parametrize('label_y', [properties.undefined, 'Label 2'])
@pytest.mark.parametrize('label_z', [properties.undefined, 'Label 3'])
@pytest.mark.parametrize(
    'manifest_cls', [manifests.View, manifests.ViewMetadata]
)
def test_good_viewmetadata(
        manifest_cls, name, description, label_x, label_y, label_z
):
    view = manifest_cls(
        name=name,
        description=description,
        label_x=label_x,
        label_y=label_y,
        label_z=label_z,
    )
    assert view.validate()


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        ('name', 'a' * 301),
        ('description', 'a' * 5001),
        ('label_x', 'a' * 301),
        ('label_y', 'a' * 301),
        ('label_z', 'a' * 301),
    ]
)
@pytest.mark.parametrize(
    'manifest_cls', [manifests.View, manifests.ViewMetadata]
)
def test_bad_viewmetadata(manifest_cls, prop, bad_val):
    """Construct and validate a simple view"""
    view = manifest_cls()
    with pytest.raises(properties.ValidationError):
        setattr(view, prop, bad_val)
        view.validate()


@pytest.mark.parametrize(
    'contents', [
        [
            'https://example.com/api/files/array/abc123',
            'https://example.com/api/elements/pointset/def456'
        ], [files.Image(content_length=100)]
    ]
)
@pytest.mark.parametrize(
    'elements', [
        [
            'https://example.com/api/elements/volumegrid/abc123',
            'https://example.com/api/elements/pointset/def456'
        ],
        [
            spatial.ElementPointSet(
                vertices='https://example.com/api/files/array/abc123'
            )
        ]
    ]
)
def test_good_view(contents, elements):
    view = manifests.View(
        contents=contents,
        elements=elements,
    )
    assert view.validate()


@pytest.mark.parametrize(
    ('prop', 'bad_val'), [
        (
            'elements', [
                'https://example.com/api/files/array/abc123',
                'https://example.com/api/elements/pointset/def456'
            ]
        ),
        (
            'elements',
            ['https://example.com/api/elements/pointset/def456'] * 101
        ),
        ('elements', [files.Image(content_length=100)]),
    ]
)
def test_bad_view(prop, bad_val):
    view = manifests.View()
    with pytest.raises(properties.ValidationError):
        setattr(view, prop, bad_val)
        view.validate()
