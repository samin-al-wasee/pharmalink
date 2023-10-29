from .utils import get_path_objects


class PathValidationMixin:
    """
    Add functionality to check the availability of resources referenced using path variables before processing the request.
    """

    def check_permissions(self, request):
        self.kwarg_objects = get_path_objects(
            request_kwargs=self.kwargs,
            path_variables=self.path_variables,
            model_classes=self.model_classes,
        )
        return super().check_permissions(request)
