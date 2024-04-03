import tempfile
from pathlib import Path
from shutil import copyfile, copytree

import aws_cdk as cdk
import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_lambda_python_alpha as python
import tomllib


class ApiStack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = Path.cwd()
            copytree(cwd.joinpath("src").absolute(), tmpdir, dirs_exist_ok=True)
            for f in ["poetry.lock", "pyproject.toml"]:
                copyfile(cwd.joinpath(f), f"{tmpdir}/{f}")

            with open(f"{tmpdir}/pyproject.toml", "rb") as f:
                _META = tomllib.load(f)

            version = _META["tool"]["poetry"]["version"]
            lambda_function = python.PythonFunction(
                self,
                "Function",
                entry=tmpdir,
                runtime=lambda_.Runtime.PYTHON_3_12,
                index="app/sst.py",
                environment={"application_version": version},
                bundling=python.BundlingOptions(
                    asset_excludes=["tests", ".ruff_cache", ".pytest_cache", "__pycache__"],
                ),
            )

        apigateway.LambdaRestApi(self, "API", handler=lambda_function)
