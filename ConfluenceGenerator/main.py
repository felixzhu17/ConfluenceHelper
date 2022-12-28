from atlassian import Confluence
import base64
import requests
from jinja2 import Template
import logging
from .process import process_confluence_template_args


class ConfluenceGenerator(Confluence):
    def __init__(self, base_url, username, api_token):
        self.base_url = base_url
        self.username = username
        self.api_token = api_token
        Confluence.__init__(
            self,
            url=self.base_url,
            username=self.username,
            password=self.api_token,
            cloud=True,
        )

    def create_or_update_page(
        self,
        title: str,
        parent_id: str,
        overwrite: bool = False,
        representation="storage",
    ):
        """Create or update a Confluence page as the experiment report

        Args:
            title (str): Title of the Confluence page
            parent_id (str): ID of the parent Confluence page
            overwrite (bool): Whether to overwrite existing pages
            representation (str, optional): Representation of the Confluence page. Defaults to "storage".
        """

        space = self.get_page_space(parent_id)

        # Logger disable sandwich because of annoying logged error message if page doesn't exist.
        logging.getLogger("atlassian.confluence").disabled = True
        logging.getLogger("atlassian.rest_client").disabled = True
        page_exists = self.page_exists(space, title)
        logging.getLogger("atlassian.confluence").disabled = False
        logging.getLogger("atlassian.rest_client").disabled = False

        if page_exists:
            if not overwrite:
                raise ValueError(
                    f"{title} already exists in space {space}. Set overwrite to True to update."
                )
            page_id = self.get_page_id(space, title)
            result = self.update_page(
                parent_id=parent_id,
                page_id=page_id,
                title=title,
                body=self.xml,
                representation=representation,
            )

        else:
            result = self.create_page(
                space=space,
                parent_id=parent_id,
                title=title,
                body=self.xml,
                representation=representation,
                editor="v2",
            )
            page_id = result["id"]

        print(
            f"Your Confluence page has been uploaded at {self.base_url}/wiki/spaces/{result['space']['key']}/pages/{result['id']}"
        )
        return

    def get_page_body(self, page_id):
        auth = self.username + ":" + self.api_token
        encoded_auth = base64.b64encode(auth.encode()).decode()
        url = f"{self.base_url}/wiki/rest/api/content/{page_id}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_auth}",
        }
        response = requests.get(
            url, headers=headers, params={"expand": ["body.storage"]}
        ).json()
        return response["body"]["storage"]["value"]

    def update_confluence_template(self, title, page_id, **kwargs):

        kwargs, image_list = process_confluence_template_args(kwargs)
        upload_xml = Template(self.get_page_body(page_id)).render(**kwargs)
        result = self.create_or_update_page(
            title=title,
            parent_id=page_id,
            body=upload_xml,
            representation="storage",
        )

        for fig_name, fig in image_list:
            self.attach_file(
                fig,
                name=fig_name,
                page_id=page_id,
                space=result["space"]["key"],
                title=title,
            )

        print(
            f"Your Confluence page has been uploaded at {self.base_url}/wiki/spaces/{result['space']['key']}/pages/{result['id']}"
        )
        return
